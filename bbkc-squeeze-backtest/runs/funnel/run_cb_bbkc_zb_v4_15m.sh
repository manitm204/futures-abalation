#!/usr/bin/env bash
# Squeeze v4 on ZB (3,840 configs, 15m): develop -> validate -> luck benchmark. Resumable.
set -euo pipefail
id=cb_bbkc_zb_v4_15m; cfg=configs/funnel/cb_bbkc_funnel_zb_v4_15m.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 6
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 6
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id done $(date -u +%FT%TZ)"
