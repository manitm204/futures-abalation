#!/usr/bin/env bash
# Drift burst v2 (1-minute day session, 10,368 configs) on ES: develop -> validate -> luck benchmark -> export. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=db_es_v2 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/db_es_v2.log -p StandardError=file:$PWD/runs/db_es_v2.log runs/funnel/run_db_es_v2.sh
set -euo pipefail
id=db_es_v2; cfg=configs/funnel/db_funnel_es_v2.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_db_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_db_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_db_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id export $(date -u +%FT%TZ)"
.venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg
python3 ../futures-results/build.py
echo "=== $id done $(date -u +%FT%TZ)"
