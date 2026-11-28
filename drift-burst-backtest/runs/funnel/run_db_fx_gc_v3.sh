#!/usr/bin/env bash
# Drift burst v3 (1,296 configs) on 6E then GC: develop -> validate. No holdout.
set -uo pipefail
for m in 6e gc; do
  id=db_${m}_v3; cfg=configs/funnel/db_funnel_${m}_v3.yaml
  echo "=== $id develop $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_db_funnel.py develop --experiment-id $id --config $cfg --n-workers 8 || echo "DEVELOP FAILED $id"
  echo "=== $id validate $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_db_funnel.py validate --experiment-id $id --config $cfg --n-workers 8 || true
done
echo "=== all done $(date -u +%FT%TZ)"
