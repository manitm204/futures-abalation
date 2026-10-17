"""Silver Bullet signal generation: FVG (within a tradable window) + a prior
liquidity sweep in the same direction, optionally confirmed by a market
structure shift, optionally filtered by higher-timeframe bias.

Every FVG detected by the feature layer is a "setup candidate." Each candidate
either becomes an eligible signal or is recorded in the rejected-setups table
with a specific reason -- nothing is silently dropped.
"""

from __future__ import annotations

from datetime import datetime, timedelta

import polars as pl

from src.data.calendars import TradingCalendar
from src.features.bias import resolve_bias
from src.features.swings import available_swings_as_of
from src.strategies.ict_silver_bullet.config import SilverBulletConfig
from src.strategies.ict_silver_bullet.exits import ExitContext, resolve_stop, resolve_target, validate_stop_geometry
from src.utils.config_models import DEFAULT_SILVER_BULLET_WINDOWS
from src.utils.time import NY_TZ

INTERVAL_MINUTES = {"1min": 1, "5min": 5, "15min": 15}


def _window_end_ts_utc(session_date_ny, window_name: str, sample_bar_open_ts_ny: datetime) -> datetime:
    windows_by_name = {w.name: w for w in DEFAULT_SILVER_BULLET_WINDOWS}
    w = windows_by_name[window_name]
    end_local = datetime.combine(session_date_ny, w.end, tzinfo=NY_TZ)
    return end_local.astimezone(sample_bar_open_ts_ny.tzinfo if sample_bar_open_ts_ny.tzinfo else NY_TZ)


def generate_signals(
    features: dict[str, pl.DataFrame],
    *,
    config: SilverBulletConfig,
    config_id: str,
    strategy_version: str = "1.0.0",
    dataset_version: str = "unknown",
    daily_df: pl.DataFrame | None = None,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    bars = features["bars"]
    fvgs = features["fvgs"]
    swings = features["swings"]
    levels = features["levels"]
    sweeps = features["sweeps"]
    mss = features["mss"]

    signal_rows: list[dict] = []
    rejected_rows: list[dict] = []

    if fvgs.is_empty():
        return _empty_signals(), _empty_rejections()

    interval_minutes = INTERVAL_MINUTES[config.entry_timeframe]
    sweeps_by_dir = {
        d: sweeps.filter(pl.col("direction") == d) for d in ("bullish", "bearish")
    } if not sweeps.is_empty() else {"bullish": sweeps, "bearish": sweeps}
    mss_by_sweep = {row["sweep_id"]: row for row in mss.iter_rows(named=True)} if not mss.is_empty() else {}

    # Precomputed once instead of a per-FVG Polars .filter() call (found via
    # profiling a config that generated 15,158 signals on the full 8-year
    # history -- two per-FVG .filter() calls on `bars` dominated runtime at that
    # scale, even though each individual call looks cheap on small samples).
    bar_lookup: dict = {
        ts: (ts_ny, atr_val)
        for ts, ts_ny, atr_val in zip(
            bars["bar_open_ts"].to_list(), bars["bar_open_ts_ny"].to_list(), bars["atr"].to_list()
        )
    }

    for fvg in fvgs.iter_rows(named=True):
        base = {
            "signal_id": f"sig_{fvg['fvg_id']}",
            "config_id": config_id,
            "dataset_version": dataset_version,
            "strategy_version": strategy_version,
            "symbol": fvg["symbol"],
            "direction": "long" if fvg["direction"] == "bullish" else "short",
            "window": fvg["sb_window"],
            "setup_ts": fvg["bar1_open_ts"],
            "confirmation_ts": fvg["confirmation_ts"],
            "fvg_id": fvg["fvg_id"],
            "session_date_ny": fvg["session_date_ny"],
            # Every rejected-setup row must share an identical key set regardless
            # of which branch below rejects it -- Polars infers a DataFrame's
            # schema from the first rows and raises a ComputeError if a later
            # row has a different shape (found running the full 8-year history,
            # where enough rejection branches fire to expose the mismatch; a
            # small sample happened not to trigger it). sweep_id/bias default to
            # None and are overwritten only where meaningful.
            "sweep_id": None,
            "bias": None,
        }

        if fvg["sb_window"] not in config.windows:
            rejected_rows.append({**base, "rejection_reason": "window_not_tradable"})
            continue

        matching_sweeps = sweeps_by_dir.get(fvg["direction"])
        candidate_sweep = None
        if matching_sweeps is not None and not matching_sweeps.is_empty():
            eligible = matching_sweeps.filter(pl.col("confirmation_ts") <= fvg["bar1_open_ts"])
            if not eligible.is_empty():
                candidate_sweep = eligible.sort("confirmation_ts", descending=True).row(0, named=True)
        if candidate_sweep is None:
            rejected_rows.append({**base, "rejection_reason": "no_matching_sweep"})
            continue

        candidate_mss = mss_by_sweep.get(candidate_sweep["sweep_id"])
        if config.require_market_structure_shift and candidate_mss is None:
            rejected_rows.append({**base, "rejection_reason": "no_mss_confirmation", "sweep_id": candidate_sweep["sweep_id"]})
            continue

        # entry price / rule
        if config.fvg_entry_rule == "proximal":
            entry_price, entry_order_type = fvg["proximal"], "limit"
        elif config.fvg_entry_rule == "midpoint":
            entry_price, entry_order_type = fvg["midpoint"], "limit"
        elif config.fvg_entry_rule == "distal":
            entry_price, entry_order_type = fvg["distal"], "limit"
        elif config.fvg_entry_rule == "first_touch":
            if fvg["first_touch_ts"] is None:
                rejected_rows.append({**base, "rejection_reason": "fvg_never_touched"})
                continue
            entry_price, entry_order_type = None, "market"
        else:
            raise ValueError(f"Unsupported fvg_entry_rule: {config.fvg_entry_rule}")

        earliest_entry_ts = fvg["confirmation_ts"]
        if candidate_mss is not None:
            earliest_entry_ts = max(earliest_entry_ts, candidate_mss["break_bar_open_ts"])
        if config.fvg_entry_rule == "first_touch":
            earliest_entry_ts = max(earliest_entry_ts, fvg["first_touch_ts"])

        sample_ts_ny_val, atr_val = bar_lookup.get(fvg["bar3_open_ts"], (None, None))
        window_end_ts = (
            _window_end_ts_utc(fvg["session_date_ny"], fvg["sb_window"], earliest_entry_ts)
            if sample_ts_ny_val is not None
            else earliest_entry_ts
        )
        entry_expiration_ts = window_end_ts
        if config.fvg_max_age_bars is not None:
            age_cutoff = fvg["confirmation_ts"] + timedelta(minutes=config.fvg_max_age_bars * interval_minutes)
            entry_expiration_ts = min(entry_expiration_ts, age_cutoff)

        if earliest_entry_ts >= entry_expiration_ts:
            rejected_rows.append({**base, "rejection_reason": "expired_before_eligible"})
            continue

        bias_value = "neutral"
        if config.bias_mode != "none":
            resolved = resolve_bias(config.bias_mode, as_of_ts=earliest_entry_ts, daily_df=daily_df)
            if resolved is None:
                rejected_rows.append({**base, "rejection_reason": "bias_unresolvable"})
                continue
            bias_value = resolved
            wanted = "bullish" if fvg["direction"] == "bullish" else "bearish"
            if bias_value not in (wanted, "neutral"):
                rejected_rows.append({**base, "rejection_reason": "bias_mismatch", "bias": bias_value})
                continue

        avail_swings = available_swings_as_of(swings, earliest_entry_ts)
        opposing_level_price = None
        if config.target_type == "liquidity" and not levels.is_empty():
            want_type = "swing_low" if fvg["direction"] == "bearish" else "swing_high"
            opp = levels.filter(
                (pl.col("availability_ts") <= earliest_entry_ts) & (pl.col("type") == want_type)
            )
            if not opp.is_empty():
                if fvg["direction"] == "bullish":
                    opp = opp.filter(pl.col("price") > (entry_price or fvg["midpoint"]))
                    opposing_level_price = opp["price"].min() if not opp.is_empty() else None
                else:
                    opp = opp.filter(pl.col("price") < (entry_price or fvg["midpoint"]))
                    opposing_level_price = opp["price"].max() if not opp.is_empty() else None

        ctx = ExitContext(
            direction=fvg["direction"],
            entry_price=entry_price if entry_price is not None else fvg["midpoint"],
            fvg_distal=fvg["distal"],
            fvg_proximal=fvg["proximal"],
            swept_extreme=candidate_sweep["penetration_price"],
            mss_reference_price=candidate_mss["reference_price"] if candidate_mss else None,
            atr=atr_val,
            opposing_level_price=opposing_level_price,
        )
        stop_price = resolve_stop(config, ctx)
        if stop_price is None:
            rejected_rows.append({**base, "rejection_reason": "stop_unresolvable"})
            continue
        if not validate_stop_geometry(fvg["direction"], ctx.entry_price, stop_price):
            rejected_rows.append({**base, "rejection_reason": "invalid_stop_geometry"})
            continue

        target_price = resolve_target(config, ctx, stop_price=stop_price)
        if config.target_type == "liquidity" and target_price is None:
            rejected_rows.append({**base, "rejection_reason": "no_opposing_liquidity_target"})
            continue

        signal_rows.append(
            {
                **base,
                "earliest_entry_ts": earliest_entry_ts,
                "entry_expiration_ts": entry_expiration_ts,
                "entry_order_type": entry_order_type,
                "entry_price": entry_price,
                "stop_price": stop_price,
                "target_price": target_price,
                "sweep_id": candidate_sweep["sweep_id"],
                "mss_id": candidate_mss["mss_id"] if candidate_mss else None,
                "bias_mode": config.bias_mode,
                "bias_value": bias_value,
                "atr": atr_val,
                "fvg_size_points": fvg["size_points"],
                "fvg_size_atr_multiple": fvg["size_atr_multiple"],
            }
        )

    return (
        pl.DataFrame(signal_rows) if signal_rows else _empty_signals(),
        pl.DataFrame(rejected_rows) if rejected_rows else _empty_rejections(),
    )


def _empty_signals() -> pl.DataFrame:
    return pl.DataFrame(
        schema={
            "signal_id": pl.Utf8, "config_id": pl.Utf8, "symbol": pl.Utf8, "direction": pl.Utf8,
            "window": pl.Utf8, "earliest_entry_ts": pl.Datetime("us", "UTC"),
            "entry_expiration_ts": pl.Datetime("us", "UTC"), "entry_order_type": pl.Utf8,
            "entry_price": pl.Float64, "stop_price": pl.Float64, "target_price": pl.Float64,
        }
    )


def _empty_rejections() -> pl.DataFrame:
    return pl.DataFrame(schema={"signal_id": pl.Utf8, "symbol": pl.Utf8, "rejection_reason": pl.Utf8})
