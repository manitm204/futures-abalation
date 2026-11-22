#!/usr/bin/env bash
# Turn-of-month long v2 (1-minute bars 08:00-17:00 ET, 4,864 configs) on ES: develop -> validate -> placebo benchmark -> export. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=me_es_v2 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/me_es_v2.log -p StandardError=file:$PWD/runs/me_es_v2.log runs/funnel/run_me_es_v2.sh
set -euo pipefail
id=me_es_v2; cfg=configs/funnel/me_funnel_es_v2.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_me_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_me_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
if [ -s runs/funnel/$id/validation_results.json ]; then
  echo "=== $id placebo $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_me_random_benchmark.py --experiment-id $id --config $cfg
fi
echo "=== $id export $(date -u +%FT%TZ)"
.venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg
python3 ../futures-results/build.py
echo "=== $id done $(date -u +%FT%TZ)"
