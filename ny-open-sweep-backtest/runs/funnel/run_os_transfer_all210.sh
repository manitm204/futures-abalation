#!/usr/bin/env bash
# All 210 NQ validation survivors, unchanged, on ES / YM / RTY / GC; development + validation only (no holdout).
set -euo pipefail
for SYM in ES YM RTY GC; do
  echo "=== $SYM $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_os_transfer_check.py --manifest runs/funnel/os_nq_v1/selection_manifest.json \
    --config configs/funnel/os_funnel_nq_v1.yaml --symbol $SYM --phases development,validation --workers 6 --tag all210
done
echo "=== done $(date -u +%FT%TZ)"
