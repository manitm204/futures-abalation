#!/usr/bin/env bash
# Squeeze v3 on NQ: 15m then 5m, each develop -> validate -> luck benchmark.
set -euo pipefail
for v in 15m 5m; do
  id=cb_bbkc_nq_v3_$v; cfg=configs/funnel/cb_bbkc_funnel_nq_v3_$v.yaml
  echo "=== $id develop $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
  echo "=== $id validate $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
  echo "=== $id luck $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
  echo "=== $id done $(date -u +%FT%TZ)"
done
echo "=== ALL DONE"
