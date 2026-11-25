#!/usr/bin/env bash
# NR-N v5 close-entry ablation grids. usage: run_cb_nr_v5.sh <sym> <tf>   (no holdout)
set -euo pipefail
s=$1; t=$2; id=cb_nr_${s}_v5_${t}; cfg=configs/funnel/cb_nr_funnel_${s}_v5_${t}.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 6
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 6
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id done $(date -u +%FT%TZ)"
