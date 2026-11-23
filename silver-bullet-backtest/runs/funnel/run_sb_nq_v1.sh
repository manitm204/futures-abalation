#!/usr/bin/env bash
# ICT Silver Bullet / 2022 Model v1 (1-minute bars, 1,728 configs) on NQ: develop -> validate. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=sb_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/sb_nq_v1.log -p StandardError=file:$PWD/runs/sb_nq_v1.log runs/funnel/run_sb_nq_v1.sh
set -euo pipefail
id=sb_nq_v1; cfg=configs/funnel/sb_funnel_nq_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_sb_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_sb_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
