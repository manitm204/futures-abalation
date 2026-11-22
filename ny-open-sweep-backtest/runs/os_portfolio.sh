#!/usr/bin/env bash
set -euo pipefail
args=(--leg os_nq_v1:64 --leg os_nq_v1:195 --key open_sweep_portfolio_nq_v1 --label "#64 + #195" --market-name "E-mini Nasdaq-100")
echo "=== 2018-2024 $(date -u +%FT%TZ)"
.venv/bin/python scripts/build_os_portfolio.py "${args[@]}"
echo "=== holdout $(date -u +%FT%TZ)"
.venv/bin/python scripts/build_os_portfolio.py "${args[@]}" --holdout --confirm-holdout-access
echo "=== done $(date -u +%FT%TZ)"
