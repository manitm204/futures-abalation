#!/usr/bin/env bash
# FX fix v1 (1-minute bars, 405 configs) on 6J: develop -> validate -> luck benchmark -> export. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=fx_6j_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/fx_6j_v1.log -p StandardError=file:$PWD/runs/fx_6j_v1.log runs/funnel/run_fx_6j_v1.sh
set -euo pipefail
id=fx_6j_v1; cfg=configs/funnel/fx_funnel_6j_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_fx_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_fx_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_fx_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id export $(date -u +%FT%TZ)"
.venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg
python3 ../futures-results/build.py
echo "=== $id done $(date -u +%FT%TZ)"
