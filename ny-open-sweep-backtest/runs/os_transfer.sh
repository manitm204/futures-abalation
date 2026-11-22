#!/usr/bin/env bash
set -euo pipefail
for s in ES YM RTY; do
  echo "=== $s $(date -u +%FT%TZ)"
  .venv/bin/python scripts/run_os_transfer_check.py --manifest runs/funnel/os_nq_v1/selection_manifest_64.json \
    --config configs/funnel/os_funnel_nq_v1.yaml --symbol $s --confirm-holdout-access 2>&1 | grep -v "^\s*$" | grep -E "wrote|$s (development|validation|holdout)|Error|Traceback" || true
done
echo "=== done"
