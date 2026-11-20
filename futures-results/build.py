"""Build one self-contained results page per strategy family:
  mean reversion/index.html        mean-reversion runs, their portfolios and the all-markets pages
  noise-band breakout/index.html   noise-band breakout runs
  bb-kc squeeze/index.html         BB-inside-KC squeeze breakout (../bbkc-squeeze-backtest/)
  nr squeeze/index.html            NR-N squeeze breakout (../nr-squeeze-backtest/)
  price-path convexity/index.html  price-path convexity fade (../price-path-convexity-backtest/)
  emrt spread/index.html           EMRT two-leg futures spread (../emrt-spread-backtest/); its tabs are pairs
  fx fix/index.html                daytime FX-fix reversal around the London fix (../fx-fix-backtest/)

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
# Pair "markets" (two-leg strategies only): data/<A-B>/.
PAIRS = [("ES-NQ", "ES vs NQ"), ("ES-RTY", "ES vs RTY"), ("ES-YM", "ES vs YM"), ("ZN-ZB", "ZN vs ZB")]


# (folder, page title, header text, which runs belong) -- every page uses template.html.
FAMILIES = [
    ("mean reversion", "Mean Reversion Funnels", "Mean-reversion strategy funnels",
     lambda run: not run["strategy_key"].startswith(("noise_band", "squeeze_breakout", "nr_breakout", "path_convexity",
                                                       "emrt_spread", "fx_fix"))),
    ("noise-band breakout", "Noise-Band Breakout Funnels", "Noise-band breakout strategy funnels",
     lambda run: run["strategy_key"].startswith("noise_band")),
    ("bb-kc squeeze", "BB-inside-KC Squeeze Funnels", "BB-inside-KC squeeze strategy funnels",
     lambda run: run["strategy_key"].startswith("squeeze_breakout")),
    ("nr squeeze", "NR-N Squeeze Funnels", "NR-N squeeze strategy funnels",
     lambda run: run["strategy_key"].startswith("nr_breakout")),
    ("price-path convexity", "Price-Path Convexity Funnels", "Price-path convexity strategy funnels",
     lambda run: run["strategy_key"].startswith("path_convexity")),
    ("emrt spread", "EMRT Spread Funnels", "EMRT two-leg spread strategy funnels",
     lambda run: run["strategy_key"].startswith("emrt_spread")),
    ("fx fix", "FX Fix Funnels", "FX-fix reversal strategy funnels",
     lambda run: run["strategy_key"].startswith("fx_fix")),
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
        if not mine:  # a family with no runs yet gets no page
            continue
        # The all-markets tab only appears on a page that has all-markets results.
        if any("-" in r["market"] for r in mine):  # a pair family: its tabs are the pairs
            markets = [(c, n) for c, n in PAIRS]
        else:
            markets = [(c, n) for c, n in MARKETS if c != "ALL" or any(r["market"] == "ALL" for r in mine)]
        # A page whose all-markets runs all share one market_name (e.g. "Holdout results") shows that as the tab name.
        all_names = {r["market_name"] for r in mine if r["market"] == "ALL"}
        if len(all_names) == 1:
            markets = [(c, next(iter(all_names)) if c == "ALL" else n) for c, n in markets]
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
