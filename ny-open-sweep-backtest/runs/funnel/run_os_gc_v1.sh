#!/usr/bin/env bash
# NY-open sweep, GC-native v1 (COMEX 08:20-13:30 session, 648 configs): develop -> validate. No holdout.
#   systemd-run --user --unit=os_gc_v1 --working-directory=$PWD --setenv=PYTHONPATH=. --setenv=OS_SESSION=comex \
#       -p StandardOutput=file:$PWD/runs/os_gc_v1.log -p StandardError=file:$PWD/runs/os_gc_v1.log runs/funnel/run_os_gc_v1.sh
set -euo pipefail
export OS_SESSION=comex
id=os_gc_v1; cfg=configs/funnel/os_funnel_gc_v1.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_os_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id done $(date -u +%FT%TZ)"
