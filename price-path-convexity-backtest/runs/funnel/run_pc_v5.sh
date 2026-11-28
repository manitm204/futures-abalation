#!/bin/bash
# Price-path convexity v5 on NQ then ES: develop (stages 1-7) and validate (stage 8). No holdout.
cd "$(dirname "$0")/../.."
export PYTHONPATH=.
for S in nq es; do
  .venv/bin/python scripts/run_pc_funnel.py develop  --experiment-id pc_${S}_v5_15m --config configs/funnel/pc_funnel_${S}_v5_15m.yaml --n-workers 10 || exit 1
  .venv/bin/python scripts/run_pc_funnel.py validate --experiment-id pc_${S}_v5_15m --config configs/funnel/pc_funnel_${S}_v5_15m.yaml || exit 1
done
