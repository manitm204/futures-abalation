#!/usr/bin/env bash
# Squeeze v2 on ES, 5m grid (re-specified, 72,576 configs): develop -> validate -> luck benchmark.
set -euo pipefail
id=cb_bbkc_es_v2_5m; cfg=configs/funnel/cb_bbkc_funnel_es_v2_5m.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_funnel.py validate --experiment-id $id --config $cfg --n-workers 8
echo "=== $id luck $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_cb_random_benchmark.py --experiment-id $id --config $cfg
echo "=== $id done $(date -u +%FT%TZ)"
