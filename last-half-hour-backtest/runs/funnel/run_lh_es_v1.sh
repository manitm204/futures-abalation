#!/usr/bin/env bash
# Last-half-hour momentum v1 (1-minute RTH bars, 500 configs) on ES: develop -> validate -> luck benchmark -> export. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=lh_es_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/lh_es_v1.log -p StandardError=file:$PWD/runs/lh_es_v1.log runs/funnel/run_lh_es_v1.sh
set -euo pipefail
id=lh_es_v1; cfg=configs/funnel/lh_funnel_es_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_lh_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_lh_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
if [ -s runs/funnel/$id/validation_results.json ]; then
  echo "=== $id luck $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_lh_random_benchmark.py --experiment-id $id --config $cfg
fi
echo "=== $id export $(date -u +%FT%TZ)"
.venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg
python3 ../futures-results/build.py
echo "=== $id done $(date -u +%FT%TZ)"
