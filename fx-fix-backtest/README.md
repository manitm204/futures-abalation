# FX-Fix Reversal Screening Funnel

A daytime 6E (Euro FX) strategy built on the **FX-fix W-pattern** from Krohn, Mueller & Whelan,
"Foreign Exchange Fixings and Returns Around the Clock", *Journal of Finance* 79(1), 2024
([Bank of Canada SWP 2021-48](https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf)).
It was picked from the research survey (`../reports/Distinct futures strategy papers.md`, pick 1)
and cut down to the daytime legs, because the user does not trade overnight.

It uses the same funnel, thresholds, data splits and costs as the mean-reversion, noise-band,
squeeze and convexity studies. It was cloned from `../price-path-convexity-backtest/` on
2026-11-20. What is new:
- the base strategy (`src/strategies/fx_fix/`)
- its grid (`src/experiments/fx_grid.py`)
- its integrity checks (`src/experiments/fx_integrity.py`)
- its bars: 1-minute bars from 08:00 to 17:00 ET

This project has its own configs (`configs/funnel/fx_funnel_*.yaml`), runs and data-access ledger.
No FX-fix run has been made yet.

**This is a research tool.** Nothing here establishes or implies that any strategy is
profitable. Its purpose is to determine what does and does not survive rigorous, causal,
out-of-sample testing.

## The idea

Big FX benchmark fixes create predictable dollar demand at known times. Dealers pre-hedge into
the fix, so **the USD rises into a fix and falls after it**. Around the clock this gives a
W-shaped return path. In the paper (spot, 1999–2019):
- The post-London reversal held up after half the spot spread ($1 → $6.08 in EUR).
- The Tokyo legs decayed after about 2013.
- The same pattern shows up in CME futures from 2006.

6E is quoted in dollars per euro, so **long 6E = short the dollar**.

The paper's windows (ET) and what this project does with them:

| Window | ET | Paper's sign for the USD | Here |
|---|---|---|---|
| pre-Tokyo / post-Tokyo | 17:00–02:00 | up / down | **left out** (overnight) |
| pre-ECB | 02:00–08:15 | up (strongest net leg) | **left out** (overnight) |
| ECB → London | 08:15–11:00 | no clear sign | `pre` leg: short 6E (exploratory) |
| post-London | 11:00–17:00 | down (robust net leg) | `post` leg: long 6E |

## Rules (v1)

1. **Clock.** Each session date gets its fixes in their own time zones, converted to New York:
   - London 16:00 Europe/London (WM/R): 11:00 ET in most weeks, 12:00 ET when only the US is on
     summer time.
   - ECB 14:15 Europe/Berlin: 08:15 ET, or 09:15 ET in those same weeks.

   Switch time S = London fix + `switch_offset`.
2. **Legs.**
   - `pre`: short 6E from the ECB fix to S.
   - `post`: long 6E from S for `post_hold` minutes, or to 17:00 ET (`eod`).
   - `both`: the pre trade, then the post trade. They never overlap.
3. **Entry**: at the open of the first 1-minute bar at or after the target time, with
   market slippage. The day is skipped if that bar opens more than 5 minutes late (a gap in
   the bars).
4. **Exit**: at the close of the last bar opening before the exit time. Optional stop at a
   percent of the entry price, live intrabar. Everything is flat by 17:00 ET; bars outside
   08:00–17:00 ET are never loaded.
5. **Vol gate** (optional), known before the day starts:
   - v = daily realized vol from 5-minute closes between 08:00 and 17:00 ET.
   - g = mean of v over the previous 20 days.
   - `high` trades only when g is above its 250-day median, `low` only when g is at or below it.

   The paper finds bigger reversals in volatile periods; `low` is the control.

`src/strategies/fx_fix/backtest.py` has the full execution rules.

## v1 grid (405 configs per contract)

| Axis | Values |
|---|---|
| `leg` | post, pre, both |
| `switch_offset` | −15, −5, 0, +5, +15 min vs the London fix |
| `post_hold` | 60, 120, 240 min, eod (17:00 ET); pinned to eod for `pre` |
| `vol_gate` | none, high, low |
| `stop` | none, 0.25%, 0.50% |

Config counts: post 180 + both 180 + pre 45.

Stage 4 (local perturbation) moves one setting at a time:
- the switch time by ±5 min
- a timed hold by ±30 min
- a stop by ±0.10%

**Stage 9 transfer symbol is 6J, and it is a negative control.** The paper finds the yen moves
the *other* way after London, so 6J doing well with unchanged rules is a warning sign.

## Running

`data` and `.venv` are symlinks to `../mean-reversion-backtest/`. Large runs should go through
`systemd-run --user` so memory pressure can't take the terminal down.

```bash
PYTHONPATH=. .venv/bin/python scripts/run_fx_funnel.py develop  --experiment-id fx_6e_v1 --config configs/funnel/fx_funnel_6e_v1.yaml --n-workers 8
PYTHONPATH=. .venv/bin/python scripts/run_fx_funnel.py validate --experiment-id fx_6e_v1 --config configs/funnel/fx_funnel_6e_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/run_fx_random_benchmark.py --experiment-id fx_6e_v1 --config configs/funnel/fx_funnel_6e_v1.yaml
PYTHONPATH=. .venv/bin/python scripts/export_results_json.py --experiment-id fx_6e_v1 --config configs/funnel/fx_funnel_6e_v1.yaml
python ../futures-results/build.py        # writes ../futures-results/fx fix/index.html
PYTHONPATH=. .venv/bin/python scripts/run_fx_funnel.py final-test --manifest runs/funnel/fx_6e_v1/selection_manifest.json \
    --config configs/funnel/fx_funnel_6e_v1.yaml --confirm-holdout-access
```

- `develop` reads 2018–2022 only and freezes the representatives.
- `validate` scores the frozen set on 2023–2024.
- The random benchmark ("luck" test) places random trades of the same lengths at random times
  of the day. It asks whether the fix times matter.
- `final-test` touches 2025+ only with explicit confirmation.
- Every data access is recorded in `runs/funnel/data_access_ledger.jsonl`.
- `scripts/build_fx_portfolio.py` combines chosen finalists into one account, the same way as
  the other families' portfolio pages.

## Tests

```bash
PYTHONPATH=. .venv/bin/python -m pytest -q tests
```

`tests/unit/test_fx_fix.py` covers:
- fix times in all four daylight-saving combinations, checked against an independent pandas
  conversion
- the 08:00–17:00 bar window
- entry and exit timing for each leg, offsets and holds
- gap handling
- stops and sizing
- the vol gate against plain loops, and its causality
- the integrity checks, including that they catch tampered trades
- look-ahead truncation
- the stress knobs
- the grid, lattice, local moves and funnel config

The rest is the shared framework suite. The convexity family's tests live in
`../price-path-convexity-backtest/`.
