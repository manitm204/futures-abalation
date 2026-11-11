#!/usr/bin/env bash
# Squeeze v4 (YM's 3,840-config 15m grid) on every other market: develop -> validate -> luck.
# One market failing does not stop the rest. Resumable: re-running reuses saved prep/checkpoints.
set -uo pipefail
for m in rty cl gc 6e 6j zn es nq; do
  id=cb_bbkc_${m}_v4_15m; cfg=configs/funnel/cb_bbkc_funnel_${m}_v4_15m.yaml
  if [ -f runs/funnel/$id/random_benchmark.json ]; then echo "=== $id already done"; continue; fi
  echo "=== $id develop $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 6 || { echo "=== $id FAILED develop"; continue; }
  echo "=== $id validate $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 6 || { echo "=== $id FAILED validate"; continue; }
  echo "=== $id luck $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg || { echo "=== $id FAILED luck"; continue; }
  echo "=== $id done $(date -u +%FT%TZ)"
done
echo "=== ALL DONE $(date -u +%FT%TZ)"
