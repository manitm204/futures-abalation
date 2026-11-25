#!/usr/bin/env bash
# NY-open sweep, GC v2 (09:30 NY anchor, 648 configs): develop -> validate. No holdout.
#   systemd-run --user --unit=os_gc_v2 --working-directory=$PWD --setenv=PYTHONPATH=. --setenv=OS_SESSION=nyse \
#       -p StandardOutput=file:$PWD/runs/os_gc_v2.log -p StandardError=file:$PWD/runs/os_gc_v2.log runs/funnel/run_os_gc_v2.sh
set -euo pipefail
export OS_SESSION=nyse
id=os_gc_v2; cfg=configs/funnel/os_funnel_gc_v2.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
