#!/usr/bin/env bash
# Squeeze v3 on NQ, 5m only (restart after the 2026-11-11 crash; 15m already finished).
# Resumable: re-running this script reuses the saved prep and checkpoints.
set -euo pipefail
id=cb_bbkc_nq_v3_5m; cfg=configs/funnel/cb_bbkc_funnel_nq_v3_5m.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 6
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 6
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id done $(date -u +%FT%TZ)"
