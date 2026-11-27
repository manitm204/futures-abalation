#!/usr/bin/env bash
# Last-half-hour momentum v2 (1-minute RTH bars, 1,296 configs) on NQ: develop -> validate -> luck benchmark -> export. No holdout.
# Launch as its own unit so memory pressure can't take the terminal down:
#   systemd-run --user --unit=lh_nq_v2 --working-directory=$PWD --setenv=PYTHONPATH=. \
#       -p StandardOutput=file:$PWD/runs/lh_nq_v2.log -p StandardError=file:$PWD/runs/lh_nq_v2.log runs/funnel/run_lh_nq_v2.sh
set -uo pipefail
id=lh_nq_v2; cfg=configs/funnel/lh_funnel_nq_v2.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_lh_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_lh_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
