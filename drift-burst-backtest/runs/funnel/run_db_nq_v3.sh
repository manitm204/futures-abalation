#!/usr/bin/env bash
# Drift burst v3 (trimmed 1,296 configs) on NQ: develop -> validate -> luck benchmark. No holdout.
set -euo pipefail
id=db_nq_v3; cfg=configs/funnel/db_funnel_nq_v3.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_db_funnel.py develop --experiment-id $id --config $cfg --n-workers 8
echo "=== $id validate $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_db_funnel.py validate --experiment-id $id --config $cfg --n-workers 8 || true
echo "=== $id done $(date -u +%FT%TZ)"
