#!/usr/bin/env bash
# FVG after displacement v1 (1-minute bars, 24,192 configs) on NQ: develop -> validate. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=fv_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/fv_nq_v1.log -p StandardError=file:$PWD/runs/fv_nq_v1.log runs/funnel/run_fv_nq_v1.sh
set -euo pipefail
id=fv_nq_v1; cfg=configs/funnel/fv_funnel_nq_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_fv_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_fv_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
