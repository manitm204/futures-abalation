#!/usr/bin/env bash
# Turn-of-month v2 grid on RTY, DIAGNOSTIC ONLY: develop (2018-2022) -> export. Never validate or final-test this run.
set -euo pipefail
id=me_rty_v2; cfg=configs/funnel/me_funnel_rty_v2.yaml
echo "=== $id develop $(date -u +%FT%TZ)"
.venv/bin/python scripts/run_me_funnel.py develop --experiment-id $id --config $cfg --n-workers 6
echo "=== $id export $(date -u +%FT%TZ)"
.venv/bin/python scripts/export_results_json.py --experiment-id $id --config $cfg --label "Month end · v2 (diagnostic)" \
    --note "Diagnostic only: the ES v2 grid re-run on RTY 2018-2022 to compare the ablation shape with ES. Nothing here was validated or picked; RTY 2023+ was already used for ES pick #7."
echo "=== $id done $(date -u +%FT%TZ)"
