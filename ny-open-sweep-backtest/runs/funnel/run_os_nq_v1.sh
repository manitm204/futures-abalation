#!/usr/bin/env bash
# NY-open liquidity sweep v1 (1-minute bars, 24,300 configs) on NQ: develop -> validate. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=os_nq_v1 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/os_nq_v1.log -p StandardError=file:$PWD/runs/os_nq_v1.log runs/funnel/run_os_nq_v1.sh
set -euo pipefail
id=os_nq_v1; cfg=configs/funnel/os_funnel_nq_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
