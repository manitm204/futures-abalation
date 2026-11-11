"""Resumable `run_jobs`: save finished backtests while a slow stage runs, so a stopped or
crashed `develop` picks up where it left off.

Each named step (stage-4 local moves, stage-7 execution stress, ...) gets a folder
<experiment>/checkpoints/<name>/<fingerprint>/ of append-only part files. A part holds the
results finished since the previous save, keyed by a digest of the whole Job (parameters,
window, cost multiplier, delay, missed-entry fraction, seed, return series) minus its label.
The fingerprint is the run's prep fingerprint (backtester sources, costs, data partitions,
metric settings, development window), so a saved result is only reused for an identical
backtest; anything else lands in a new folder and is recomputed. Pausing is stopping the
process; resuming is running the same `develop` command again.

Kept out of funnel_prep.py on purpose: that file is hashed into the prep fingerprint, and
the checkpointing itself never changes a result.
"""

from __future__ import annotations

import hashlib
import multiprocessing
import os
import pickle
import signal
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import polars as pl

from src.experiments import funnel_prep as fp
from src.experiments.funnel_prep import Job
from src.utils.hashing import canonical_json
from src.utils.logging import get_logger
from src.utils.serialization import atomic_write_bytes

logger = get_logger(__name__)
SAVE_EVERY_S = 60.0


def job_digest(job: Job) -> str:
    """Identity of a backtest: everything in the Job except its label."""
    ident = {"params": job.params.__dict__, "start": job.window_start, "end": job.window_end,
             "cost": job.cost_multiplier, "delay": job.entry_delay_bars, "miss": job.missed_entry_frac,
             "seed": job.seed, "series": job.return_series}
    return hashlib.sha256(canonical_json(ident).encode()).hexdigest()


def _load(folder: Path) -> dict[str, dict]:
    done: dict[str, dict] = {}
    for part in sorted(folder.glob("part-*.pkl")):
        try:
            done.update(pickle.loads(part.read_bytes()))
        except Exception:  # a part cut off mid-write by a crash: its jobs are simply re-run
            logger.warning("checkpoint_part_unreadable", part=str(part))
    return done


def _imap(jobs, frames, *, fcfg, exec_config, n_workers):
    """Like funnel_prep._pool_map(_job_worker, ...) but yields results as they finish (in order)."""
    if n_workers <= 1 or len(jobs) < 8:
        fp._init({}, fcfg, exec_config)
        for k, df in frames.items():
            fp._DATA[k] = fp.family_for(fcfg).data_cls(df)
        for j in jobs:
            yield fp._job_worker(j)
        return
    with tempfile.TemporaryDirectory() as td:
        paths = {}
        for k, df in frames.items():
            p = str(Path(td) / f"{k.replace('|', '_')}.parquet")
            df.write_parquet(p)
            paths[k] = p
        ctx = multiprocessing.get_context("spawn")
        with ProcessPoolExecutor(max_workers=n_workers, mp_context=ctx, initializer=fp._init,
                                 initargs=(paths, fcfg, exec_config)) as ex:
            yield from ex.map(fp._job_worker, jobs, chunksize=4)


def run_jobs_checkpointed(jobs: list[Job], frames: dict[str, pl.DataFrame], *, fcfg, exec_config,
                          n_workers: int, root: Path, name: str, fingerprint: str,
                          resume: bool = True) -> dict[str, dict]:
    """Same result as funnel_prep.run_jobs, saving progress under root/name/fingerprint."""
    if not jobs:
        return {}
    folder = root / name / fingerprint[:16]
    folder.mkdir(parents=True, exist_ok=True)
    done = _load(folder) if resume else {}
    digests = [job_digest(j) for j in jobs]
    todo = [j for j, d in zip(jobs, digests) if d not in done]
    logger.info("checkpoint_resume", step=name, total=len(jobs), saved=len(jobs) - len(todo), to_run=len(todo))
    if todo:
        n_parts = len(list(folder.glob("part-*.pkl")))
        pending: dict[str, dict] = {}
        last = time.time()

        def flush():
            nonlocal n_parts, pending, last
            if pending:
                atomic_write_bytes(folder / f"part-{n_parts:05d}.pkl", pickle.dumps(pending, protocol=5))
                n_parts += 1
                done.update(pending)
                logger.info("checkpoint_saved", step=name, saved=len(done), of=len(jobs))
                pending = {}
            last = time.time()

        def _term(signum, frame):  # `systemctl stop` / kill: unwind so the finally below saves
            raise SystemExit(128 + signum)

        old = signal.signal(signal.SIGTERM, _term)
        try:
            for j, r in zip(todo, _imap(todo, frames, fcfg=fcfg, exec_config=exec_config, n_workers=n_workers)):
                pending[job_digest(j)] = {k: v for k, v in r.items() if k != "key"}
                if time.time() - last >= SAVE_EVERY_S:
                    flush()
        finally:
            flush()  # also on Ctrl-C / SIGTERM, so a pause keeps everything finished so far
            signal.signal(signal.SIGTERM, old)
    return {j.key: {"key": j.key, **done[d]} for j, d in zip(jobs, digests)}
