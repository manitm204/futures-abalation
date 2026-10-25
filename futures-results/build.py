"""Build index.html: one self-contained page with every futures funnel result.

Layout of this folder:
  data/<MARKET>/<strategy>.json   one finished run (written by each project's export script,
                                  e.g. mean-reversion-backtest/scripts/export_results_json.py)
  notes/<MARKET>/<strategy>.html  optional hand-written findings shown above the tables
  template.html                   page shell + renderer
  index.html                      generated; open it directly in a browser (no server needed)

Adding a market or strategy = drop its JSON into data/ and re-run:
  python build.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKETS = [
    ("ES", "E-mini S&P 500"), ("NQ", "E-mini Nasdaq-100"), ("YM", "E-mini Dow"), ("RTY", "E-mini Russell 2000"),
    ("CL", "Crude oil"), ("GC", "Gold"), ("6E", "Euro FX"), ("6J", "Japanese yen"),
    ("ZN", "10-year T-note"), ("ZB", "30-year T-bond"),
]


def main() -> None:
    runs = []
    for path in sorted((HERE / "data").glob("*/*.json")):
        run = json.loads(path.read_text())
        notes = HERE / "notes" / path.parent.name / f"{path.stem}.html"
        run["notes_html"] = notes.read_text() if notes.exists() else None
        runs.append(run)
    payload = json.dumps({"markets": [{"code": c, "name": n} for c, n in MARKETS], "runs": runs})
    html = (HERE / "template.html").read_text().replace("/*__DATA__*/null", payload.replace("</", "<\\/"))
    (HERE / "index.html").write_text(html)
    print(f"index.html: {len(runs)} run(s) across {len({r['market'] for r in runs})} market(s)")


if __name__ == "__main__":
    main()
