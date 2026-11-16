#!/usr/bin/env bash
# NR-N v4 (15m, 2,304 configs) on CL: develop -> validate -> luck benchmark. No holdout.
set -euo pipefail
id=cb_nr_cl_v4_15m; cfg=configs/funnel/cb_nr_funnel_cl_v4_15m.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id done $(date -u +%FT%TZ)"
