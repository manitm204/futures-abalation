"""Build one self-contained results page per strategy family:
  mean reversion/index.html        mean-reversion runs, their portfolios and the all-markets pages
  noise-band breakout/index.html   noise-band breakout runs

Layout of this folder:
  data/<MARKET>/<strategy>.json   one finished run (written by each project's export script,
                                  e.g. mean-reversion-backtest/scripts/export_results_json.py)
  notes/<MARKET>/<strategy>.html  optional hand-written findings shown above the tables
  template.html                   page shell + renderer
  <family>/index.html             generated; open it directly in a browser (no server needed)

Adding a market or strategy = drop its JSON into data/ and re-run:
  python build.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKETS = [
    ("ALL", "All markets"), ("ES", "E-mini S&P 500"), ("NQ", "E-mini Nasdaq-100"), ("YM", "E-mini Dow"), ("RTY", "E-mini Russell 2000"),
    ("CL", "Crude oil"), ("GC", "Gold"), ("6E", "Euro FX"), ("6J", "Japanese yen"),
    ("ZN", "10-year T-note"), ("ZB", "30-year T-bond"),
]


# (folder, page title, header text, which runs belong) -- every page uses template.html.
FAMILIES = [
    ("mean reversion", "Mean Reversion Funnels", "Mean-reversion strategy funnels",
     lambda run: not run["strategy_key"].startswith("noise_band")),
    ("noise-band breakout", "Noise-Band Breakout Funnels", "Noise-band breakout strategy funnels",
     lambda run: run["strategy_key"].startswith("noise_band")),
]


def main() -> None:
    runs = []
    for path in sorted((HERE / "data").glob("*/*.json")):
        run = json.loads(path.read_text())
        if "market" not in run:  # data for a standalone page (selection_model.html, trades.html), not a run
            continue
        notes = HERE / "notes" / path.parent.name / f"{path.stem}.html"
        run["notes_html"] = notes.read_text() if notes.exists() else None
        runs.append(run)
    template = (HERE / "template.html").read_text()
    for folder, title, brand, belongs in FAMILIES:
        mine = [r for r in runs if belongs(r)]
        # The all-markets tab only appears on a page that has all-markets results.
        markets = [(c, n) for c, n in MARKETS if c != "ALL" or any(r["market"] == "ALL" for r in mine)]
        payload = json.dumps({"markets": [{"code": c, "name": n} for c, n in markets], "runs": mine})
        html = (template.replace("<title>Futures Strategy Funnels</title>", f"<title>{title}</title>")
                .replace('<div class="brand">Futures strategy funnels</div>', f'<div class="brand">{brand}</div>')
                .replace("/*__DATA__*/null", payload.replace("</", "<\\/")))
        out = HERE / folder / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(html)
        print(f"{folder}/index.html: {len(mine)} run(s) across {len({r['market'] for r in mine})} market(s)")


if __name__ == "__main__":
    main()
