#!/usr/bin/env bash
# FX fix v2 (conditioned post leg, 1,224 configs) on 6E then 6J: develop -> validate -> luck -> export. No holdout.
#   systemd-run --user --unit=fx_v2 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/fx_v2.log -p StandardError=file:$PWD/runs/fx_v2.log runs/funnel/run_fx_v2.sh
set -euo pipefail
for m in 6e 6j; do
  id=fx_${m}_v2; cfg=configs/funnel/fx_funnel_${m}_v2.yaml
  echo "=== $id develop $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_fx_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
  echo "=== $id validate $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_fx_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
  echo "=== $id luck $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_fx_random_benchmark.py --experiment-id $id --config $cfg || true
  echo "=== $id export $(date -u +%FT%TZ)"
  .venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg || true
done
echo "=== all done $(date -u +%FT%TZ)"
