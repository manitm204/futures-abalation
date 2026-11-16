# Screening funnel -- cb_nr_gc_v4_15m (development stages only)

- Code: `278b87465dd4` (dirty working tree: True, diff sha256 `234dce23ae0e`)
- Config: `configs/funnel/cb_nr_funnel_gc_v4_15m.yaml` sha256 `f017a3884420a51a`; seed 20261120
- Data loaded: 2018-01-02 .. 2022-12-30 (phase end 2022-12-31); available endpoint per manifest: {'GC': '2026-10-16', 'ES': '2026-10-16'}
- Frozen manifest sha256: `6c9ce19c040f8f10` (22 candidates)

## Data history (not untouched)

- Validation 2023-2024 previously used for selection: **True** -- GC 2023-2024 was used to select BB/KC squeeze strategies (cb_bbkc_gc_v4_15m) and mean-reversion strategies; no NR-N strategy has been selected on GC. This grid was chosen after reading NR v2/v3 on ES; it was run on GC after its NQ / YM / RTY / CL v4 results were seen.
- Holdout 2025+ previously inspected: **True** -- GC 2025+ was read for BB/KC squeeze holdout scoring (cb_bbkc_gc_v4_15m) and mean-reversion holdout scoring per the data-access ledgers. No NR-N metrics have been computed on GC 2025+.

## Survivor counts

| Stage | Kind | Evaluated | Passed | Hard reject | Insufficient evidence | Deduplicated | With warnings | % of universe | % of previous | Note |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 0 universe | universe | 2304 | 2304 |  |  |  |  | 100.00 | 100.00 |  |
| 1 backtest integrity | hard_gate | 2304 | 1132 | 1172 | 0 |  | 0 | 49.13 | 49.13 |  |
| 2 trade count & coverage | hard_gate | 1132 | 940 | 192 | 0 |  | 878 | 40.80 | 83.04 |  |
| 3 performance & risk | hard_gate | 940 | 62 | 878 | 0 |  | 0 | 2.69 | 6.60 |  |
| 4 parameter stability | hard_gate | 62 | 62 | 0 | 0 |  | 11 | 2.69 | 100.00 |  |
| 5 time stability | hard_gate | 62 | 62 | 0 | 0 |  | 62 | 2.69 | 100.00 |  |
| 6 deduplication | dedup | 62 | 22 |  |  | 40 |  | 0.95 | 35.48 | best 2 per cluster |
| 7 execution stress | hard_gate | 22 | 22 | 0 | 0 |  | 20 | 0.95 | 100.00 |  |
| 8 frozen validation | hard_gate |  |  |  |  |  |  |  |  | not run in `develop`; run the `validate` command on the frozen manifest |
| 9 DSR / transfer | diagnostic_only | 22 |  |  |  |  |  |  |  | diagnostic only: unverified: 22 |
| 10 final holdout | explicit_command |  |  |  |  |  |  |  |  | not run; `final-test` command only |

## Rejection reasons

| Stage:status:reason | Count |
|---|---:|
| s1:hard_reject:integrity:box_not_from_prior_compression_run | 1172 |
| s1:hard_reject:integrity:entry_fill_better_than_market | 976 |
| s1:hard_reject:integrity:entry_signal_condition_not_met | 662 |
| s1:hard_reject:integrity:eod_exit_not_at_session_close | 68 |
| s1:hard_reject:integrity:exit_not_at_first_touch | 280 |
| s1:hard_reject:integrity:not_first_breakout_of_run | 920 |
| s1:hard_reject:integrity:stop_exit_without_touch | 255 |
| s1:hard_reject:integrity:stop_fill_better_than_rule | 270 |
| s1:hard_reject:integrity:stop_not_per_rule | 992 |
| s1:hard_reject:integrity:target_not_per_rule | 765 |
| s1:hard_reject:integrity:target_taken_when_stop_touched | 8 |
| s2:hard_reject:completed_trades | 192 |
| s2:hard_reject:years_with_>=10_trades | 120 |
| s3:hard_reject:net_return | 250 |
| s3:hard_reject:sharpe | 878 |

## Representatives (development ordering)

Annual figures are **in-sample diagnostics**, not out-of-sample tests.

| # | config | settings | target/eod/stop exits | trades | net ret | CAGR | Sharpe | maxDD | DD days | PF | expo | turn/yr | nbr n/possible | nbr prof | nbr med SR | ctr-med | prof yrs | ex-best ret | best-yr contrib | top-k contrib | stress 1.5x | 2x | delay | miss med/p10 | BE mult | s7 | DSR (label) | ES dev SR |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---:|
| 1 | `cfg_5554` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 176/326/95 | 597 | 10.7% | 2.1% | 1.27 | -2.9% | 204 | 1.34 | 11.2% | 327.1 | 4/4 | 0.75 | 0.96 | 0.30 | 4 | 4.1% | 0.61 | 0.24 | 5.9% | 1.1% | -0.9% | 9.2%/8.1% | 2.1 (interpolated) | pass | 0.614 (unverified) | 1.25 |
| 2 | `cfg_94d9` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 178/337/99 | 614 | 10.5% | 2.0% | 1.23 | -2.9% | 204 | 1.32 | 11.4% | 335.8 | 4/4 | 0.75 | 0.95 | 0.28 | 4 | 4.1% | 0.60 | 0.24 | 5.6% | 0.5% | -2.2% | 9.1%/8.0% | 2.1 (interpolated) | pass | 0.581 (unverified) | 1.12 |
| 3 | `cfg_8df6` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 332/525/195 | 1052 | 13.9% | 2.7% | 1.19 | -3.4% | 233 | 1.22 | 19.9% | 574.7 | 4/4 | 0.75 | 0.93 | 0.26 | 3 | 4.9% | 0.66 | 0.22 | 5.4% | -2.8% | -9.0% | 12.3%/10.1% | 1.8 (interpolated) | pass | 0.547 (unverified) | 0.85 |
| 4 | `cfg_4438` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 335/531/201 | 1067 | 13.2% | 2.5% | 1.12 | -3.1% | 252 | 1.21 | 20.2% | 584.1 | 4/4 | 0.75 | 0.90 | 0.22 | 3 | 4.0% | 0.71 | 0.24 | 4.0% | -3.8% | -10.2% | 11.9%/9.4% | 1.8 (interpolated) | pass | 0.482 (unverified) | 0.61 |
| 5 | `cfg_bfd2` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=none, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 0/483/109 | 592 | 14.3% | 2.8% | 1.07 | -4.1% | 204 | 1.40 | 14.4% | 324.5 | 4/4 | 1.00 | 0.93 | 0.15 | 4 | 4.9% | 0.65 | 0.62 | 9.0% | 4.6% | 2.0% | 12.8%/9.9% | 2.5 (interpolated) | pass | 0.429 (unverified) | 1.26 |
| 6 | `cfg_426d` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=none, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 0/470/106 | 576 | 14.4% | 2.8% | 1.09 | -4.1% | 204 | 1.41 | 14.2% | 315.9 | 4/4 | 1.00 | 0.94 | 0.15 | 4 | 4.8% | 0.66 | 0.62 | 9.3% | 4.9% | 2.8% | 12.7%/10.0% | 2.6 (interpolated) | pass | 0.444 (unverified) | 1.31 |
| 7 | `cfg_3dee` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 96/696/208 | 1000 | 12.8% | 2.5% | 0.92 | -4.9% | 235 | 1.20 | 23.2% | 546.0 | 5/5 | 1.00 | 0.91 | 0.01 | 4 | 4.9% | 0.64 | 0.38 | 5.7% | -3.1% | -8.2% | 11.7%/9.7% | 1.8 (interpolated) | pass | 0.305 (unverified) | 1.01 |
| 8 | `cfg_5723` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=2.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 94/690/203 | 987 | 13.6% | 2.6% | 0.98 | -5.0% | 221 | 1.21 | 23.0% | 538.2 | 5/5 | 1.00 | 0.92 | 0.06 | 4 | 5.2% | 0.60 | 0.36 | 6.0% | -2.3% | -7.0% | 12.2%/9.5% | 1.9 (interpolated) | pass | 0.358 (unverified) | 1.20 |
| 9 | `cfg_cd75` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 47/257/23 | 327 | 6.8% | 1.3% | 0.99 | -1.8% | 194 | 1.41 | 7.2% | 175.6 | 4/4 | 1.00 | 0.76 | 0.23 | 4 | 2.4% | 0.63 | 0.46 | 4.3% | 1.8% | -2.2% | 6.4%/5.2% | 2.4 (interpolated) | pass | 0.363 (unverified) | 0.69 |
| 10 | `cfg_d85a` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 46/248/22 | 316 | 6.8% | 1.3% | 0.99 | -1.8% | 194 | 1.42 | 7.0% | 170.2 | 4/4 | 1.00 | 0.75 | 0.24 | 4 | 2.3% | 0.65 | 0.46 | 4.4% | 1.9% | -1.8% | 5.9%/4.7% | 2.4 (interpolated) | pass | 0.361 (unverified) | 0.62 |
| 11 | `cfg_3222` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 97/469/50 | 616 | 9.8% | 1.9% | 0.95 | -3.4% | 204 | 1.26 | 14.0% | 337.0 | 4/4 | 1.00 | 0.76 | 0.19 | 4 | 4.8% | 0.53 | 0.34 | 4.5% | -0.0% | -5.4% | 8.8%/6.6% | 2.0 (interpolated) | pass | 0.339 (unverified) | 0.58 |
| 12 | `cfg_0c41` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 44/103/21 | 168 | 3.4% | 0.7% | 0.89 | -0.6% | 241 | 1.49 | 3.2% | 89.6 | 4/4 | 1.00 | 0.55 | 0.34 | 4 | 2.0% | 0.40 | 0.49 | 2.1% | 0.9% | -0.8% | 3.0%/2.4% | 2.4 (interpolated) | pass | 0.290 (unverified) | 0.04 |
| 13 | `cfg_f171` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=False, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=ema200, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 95/458/49 | 602 | 9.5% | 1.9% | 0.92 | -3.8% | 204 | 1.25 | 13.8% | 329.2 | 4/4 | 1.00 | 0.71 | 0.21 | 4 | 4.3% | 0.54 | 0.36 | 4.6% | -0.2% | -5.0% | 9.1%/6.9% | 2.0 (interpolated) | pass | 0.316 (unverified) | 0.67 |
| 14 | `cfg_3228` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 84/181/46 | 311 | 4.5% | 0.9% | 0.84 | -1.3% | 205 | 1.32 | 5.9% | 167.4 | 4/4 | 1.00 | 0.58 | 0.26 | 3 | 1.6% | 0.64 | 0.49 | 2.1% | -0.2% | -2.6% | 4.0%/3.1% | 2.0 (interpolated) | pass | 0.249 (unverified) | 0.28 |
| 15 | `cfg_ab70` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 46/107/23 | 176 | 3.3% | 0.7% | 0.84 | -0.6% | 238 | 1.44 | 3.4% | 93.8 | 4/4 | 1.00 | 0.52 | 0.32 | 4 | 1.9% | 0.43 | 0.50 | 2.0% | 0.6% | -1.3% | 3.0%/2.4% | 2.2 (interpolated) | pass | 0.251 (unverified) | -0.06 |
| 16 | `cfg_5e28` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=none, min_box_atr=0.0, max_range_atr=0.5, max_hold_bars=0 | 87/192/50 | 329 | 4.5% | 0.9% | 0.83 | -1.5% | 205 | 1.30 | 6.1% | 176.5 | 4/4 | 1.00 | 0.57 | 0.26 | 3 | 1.7% | 0.62 | 0.49 | 1.9% | -0.4% | -3.3% | 3.8%/2.7% | 1.9 (interpolated) | pass | 0.240 (unverified) | 0.23 |
| 17 | `cfg_51f3` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 167/303/98 | 568 | 5.7% | 1.1% | 0.76 | -1.6% | 292 | 1.19 | 10.5% | 305.7 | 4/4 | 1.00 | 0.58 | 0.18 | 3 | 0.9% | 0.84 | 0.53 | 1.3% | -3.1% | -8.6% | 5.1%/3.9% | 1.7 (interpolated) | pass | 0.194 (unverified) | 0.19 |
| 18 | `cfg_10a3` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.5, target_r=1.0, direction=both, trend_filter=none, min_box_atr=0.3, max_range_atr=0.5, max_hold_bars=0 | 87/412/48 | 547 | 8.4% | 1.7% | 0.88 | -2.2% | 196 | 1.27 | 12.2% | 297.2 | 4/4 | 1.00 | 0.75 | 0.13 | 4 | 2.5% | 0.69 | 0.45 | 4.0% | -0.4% | -5.4% | 7.7%/6.1% | 2.0 (interpolated) | pass | 0.274 (unverified) | 0.62 |
| 19 | `cfg_2b58` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 390/58/295 | 743 | 8.8% | 1.7% | 0.90 | -3.8% | 536 | 1.19 | 9.7% | 398.8 | 4/4 | 1.00 | 0.65 | 0.25 | 3 | 1.1% | 0.85 | 0.32 | 3.1% | -2.9% | -16.0% | 7.6%/6.0% | 1.8 (interpolated) | pass | 0.300 (unverified) | 0.23 |
| 20 | `cfg_8c7f` | timeframe=15min, compression=nr, nr_lookback=2, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=box, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 393/58/298 | 749 | 8.9% | 1.7% | 0.91 | -3.9% | 536 | 1.19 | 9.8% | 401.9 | 4/4 | 1.00 | 0.64 | 0.27 | 3 | 1.1% | 0.84 | 0.31 | 3.1% | -2.9% | -16.2% | 7.5%/6.3% | 1.8 (interpolated) | pass | 0.308 (unverified) | 0.28 |
| 21 | `cfg_0bfa` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.0, max_range_atr=off, max_hold_bars=0 | 38/91/17 | 146 | 2.6% | 0.5% | 0.78 | -0.5% | 202 | 1.47 | 2.5% | 78.9 | 5/5 | 1.00 | 0.46 | 0.32 | 5 | 1.8% | 0.33 | 0.55 | 1.5% | 0.5% | -1.4% | 2.5%/1.9% | 2.2 (interpolated) | pass | 0.217 (unverified) | -0.03 |
| 22 | `cfg_afdc` | timeframe=15min, compression=nr, nr_lookback=16, inside_bar=True, min_nr_bars=1, entry_type=wick, setup_expiry_bars=1, stop=1.0, target_r=1.0, direction=long, trend_filter=ema200, min_box_atr=0.3, max_range_atr=off, max_hold_bars=0 | 36/86/15 | 137 | 2.6% | 0.5% | 0.81 | -0.5% | 202 | 1.51 | 2.4% | 74.2 | 5/5 | 1.00 | 0.48 | 0.33 | 4 | 1.6% | 0.38 | 0.56 | 1.6% | 0.5% | -1.1% | 2.3%/1.8% | 2.3 (interpolated) | pass | 0.232 (unverified) | 0.07 |

### Per-year development slices (in-sample diagnostics)

| # | 2018 ret / SR / trades | 2019 ret / SR / trades | 2020 ret / SR / trades | 2021 ret / SR / trades | 2022 ret / SR / trades |
|---|---|---|---|---|---|
| 1 | 0.7% / 0.61 / 107 | 2.0% / 1.49 / 122 | 6.3% / 2.73 / 112 | 3.0% / 2.01 / 140 | -1.6% / -0.98 / 116 |
| 2 | 0.7% / 0.62 / 109 | 1.7% / 1.23 / 125 | 6.1% / 2.63 / 114 | 3.3% / 2.19 / 148 | -1.6% / -0.97 / 118 |
| 3 | -0.1% / -0.06 / 199 | 0.7% / 0.39 / 210 | 7.2% / 2.30 / 191 | 8.5% / 3.76 / 250 | -2.6% / -1.28 / 202 |
| 4 | -0.2% / -0.14 / 200 | 0.7% / 0.38 / 211 | 5.8% / 1.85 / 196 | 8.8% / 3.83 / 252 | -2.1% / -0.96 / 208 |
| 5 | 2.4% / 1.24 / 105 | 1.6% / 0.76 / 117 | 8.9% / 2.12 / 109 | 3.5% / 1.68 / 144 | -2.5% / -1.53 / 117 |
| 6 | 2.4% / 1.25 / 104 | 1.9% / 0.91 / 114 | 9.2% / 2.17 / 107 | 3.1% / 1.51 / 136 | -2.5% / -1.56 / 115 |
| 7 | 1.4% / 0.70 / 187 | 0.3% / 0.15 / 199 | 6.6% / 1.67 / 185 | 7.6% / 2.95 / 232 | -3.3% / -1.47 / 197 |
| 8 | 1.4% / 0.70 / 187 | 0.3% / 0.15 / 198 | 8.0% / 2.03 / 180 | 7.2% / 2.85 / 230 | -3.5% / -1.64 / 192 |
| 9 | 0.6% / 0.64 / 59 | 0.1% / 0.13 / 72 | 4.2% / 2.08 / 51 | 2.6% / 2.19 / 86 | -0.9% / -0.79 / 59 |
| 10 | 0.4% / 0.48 / 58 | 0.1% / 0.11 / 71 | 4.4% / 2.14 / 49 | 2.6% / 2.14 / 81 | -0.8% / -0.70 / 57 |
| 11 | 1.0% / 0.73 / 103 | 1.6% / 0.93 / 130 | 4.8% / 1.65 / 116 | 4.8% / 2.55 / 147 | -2.6% / -1.44 / 120 |
| 12 | -0.2% / -0.47 / 23 | 1.4% / 1.73 / 41 | 1.3% / 1.24 / 34 | 0.4% / 0.55 / 45 | 0.5% / 0.77 / 25 |
| 13 | 0.9% / 0.62 / 102 | 1.6% / 0.92 / 128 | 5.0% / 1.74 / 113 | 4.8% / 2.53 / 142 | -2.9% / -1.60 / 117 |
| 14 | -0.1% / -0.15 / 61 | 1.6% / 1.68 / 66 | 2.9% / 1.89 / 49 | 0.4% / 0.46 / 76 | -0.2% / -0.25 / 59 |
| 15 | -0.1% / -0.17 / 24 | 1.0% / 1.19 / 42 | 1.4% / 1.28 / 35 | 0.6% / 0.92 / 49 | 0.3% / 0.46 / 26 |
| 16 | -0.1% / -0.15 / 63 | 1.3% / 1.28 / 68 | 2.8% / 1.87 / 52 | 0.9% / 0.96 / 85 | -0.3% / -0.34 / 61 |
| 17 | -0.7% / -0.60 / 113 | 0.8% / 0.62 / 127 | 4.7% / 2.39 / 86 | 1.7% / 1.22 / 137 | -0.9% / -0.60 / 105 |
| 18 | 0.4% / 0.29 / 108 | 0.0% / 0.02 / 121 | 5.7% / 2.10 / 84 | 3.4% / 2.10 / 133 | -1.3% / -0.83 / 101 |
| 19 | -3.3% / -2.70 / 119 | 0.9% / 0.58 / 191 | 7.6% / 2.97 / 167 | -0.6% / -0.29 / 150 | 4.1% / 2.01 / 116 |
| 20 | -3.3% / -2.73 / 120 | 0.9% / 0.58 / 191 | 7.7% / 2.98 / 168 | -0.4% / -0.23 / 153 | 4.1% / 2.00 / 117 |
| 21 | 0.1% / 0.17 / 26 | 0.7% / 1.00 / 34 | 0.9% / 1.00 / 24 | 0.5% / 0.93 / 41 | 0.5% / 0.77 / 21 |
| 22 | -0.0% / -0.05 / 25 | 1.0% / 1.77 / 33 | 0.7% / 0.78 / 22 | 0.2% / 0.49 / 37 | 0.7% / 1.10 / 20 |

### Clusters

| cluster | rep | size | min pairwise monthly corr | rep daily corr (min/med) | rep trade overlap (min/med) |
|---:|---|---:|---:|---|---|
| 0 | `cfg_3dee` | 13 | 0.92 | 0.82/0.88 | 0.85/0.88 |
| 1 | `cfg_0bfa` | 2 | 0.95 | 0.95/0.95 | 0.94/0.94 |
| 2 | `cfg_0c41` | 5 | 0.83 | 0.83/0.85 | 0.79/0.83 |
| 3 | `cfg_bfd2` | 12 | 0.89 | 0.91/0.98 | 0.89/0.93 |
| 4 | `cfg_51f3` | 6 | 0.83 | 0.70/0.80 | 0.74/0.81 |
| 5 | `cfg_cd75` | 6 | 0.94 | 0.93/0.94 | 0.88/0.93 |
| 6 | `cfg_2b58` | 2 | 1.00 | 1.00/1.00 | 1.00/1.00 |
| 7 | `cfg_3228` | 3 | 0.89 | 0.88/0.93 | 0.81/0.88 |
| 8 | `cfg_3222` | 3 | 0.86 | 0.85/0.92 | 0.88/0.93 |
| 9 | `cfg_5554` | 4 | 0.90 | 0.89/0.90 | 0.80/0.82 |
| 10 | `cfg_8df6` | 6 | 0.83 | 0.80/0.85 | 0.80/0.81 |

Deduplication removes redundant candidates; it does not erase the search or make clusters independent trials.

## Stage 9 -- DSR audit (diagnostic, not a gate)

- Return frequency: daily (all Sharpe, SR*, variance in per-period daily units; annualized x sqrt(252) for display)
- Trial-Sharpe variance (per period): 6.309e-04 over 2304 configs (every development backtest in the full grid (not survivors))
- Effective trials: Li-Ji 265.0, participation ratio 12.1, 95%-variance components 99 (rank bound T = 1239); raw grid 2304; raw + known prior 608640
- Primary method: li_ji; serial dependence: lag1_effective_n (AR(1) effective n); kurtosis passed as excess
- Calibration verified: **False** -> labels are `unverified` until reviewed

Unresolved:
- Effective-trial count is estimated from the eigen-spectrum of the full-grid development return correlation matrix; the estimate is bounded by the number of days (rank) and the choice of estimator (Li-Ji vs participation ratio) moves DSR materially.
- The earlier ICT Silver Bullet search has no recorded trial count, so it is not included in any trial total.
- Threshold changes across funnel_v1..v3 are additional researcher degrees of freedom not captured by a config count.
- Trial-Sharpe dispersion includes configs with very few trades, whose noisy Sharpe inflates the variance (and so the benchmark).

A candidate can be a research survivor (passes stages 1-7) without passing DSR; the two are reported separately.
ES results are unchanged rules on the development period: supporting evidence, not an independent replication.

## Integrity audit

- Compression at bar k uses bars through k only: bbkc = 2 x population sd(close, L) < kc_mult x Wilder ATR(L) (Bollinger 2 sd inside a Keltner channel, both centred on SMA(L)); nr = the bar's high-low range is the narrowest of the last N bars (ties count), and with inside_bar also inside the previous bar's range. Indicators run over the RTH bar series across sessions.
- A run is a maximal stretch of consecutive compression bars inside one session (never continued across the open); its box through bar r is [min low, max high] of its bars up to r. The decision at bar k uses the run holding the last compression bar r <= k-1 of k's session, live when k - r <= setup_expiry_bars, the run is at least min_squeeze_bars long (NR: min_nr_bars, 1 unless the round sets it) and the box is at least min_box_atr x ATR(14)[r] wide, so the box never includes the decision bar. A box too narrow to be live never consumes its run.
- Breakout: close entries need close_k beyond the box and fill at the NEXT bar's open (market slippage); wick entries are a stop order at the box edge, filled on bar k at the worse of its open and the edge (stop slippage); a wick bar through both edges is ambiguous and not traded. The fill bar must be in the decision's session.
- The FIRST breakout of a run decides and consumes it, traded or not (wrong direction, trend filter, inside the last 30 minutes, a position already open, a missed entry). Each setup is one decision.
- Filters known at the decision: emaN (ema20 / ema50 / ema200) needs close > EMA(N) for a long / < for a short (close entries at bar k, wick entries at bar k-1); no decision on the session's last bar or less than 30 minutes before its last close.
- Stop = the far side of the box, or entry price -/+ k x ATR(14) using the ATR known before the fill bar; R = entry price (before slippage) to stop; target = entry +/- target_r x R. Stop and target are live intrabar from the entry bar; a bar touching both counts as the stop; on a wick entry's own bar only the stop is checked, and a touch there counts (conservative). Stops fill at the worse of open and stop, targets at the better of open and target (a gap through it), each with slippage.
- Every position still open on the session's last bar is closed at that bar's CLOSE (market-on-close with the same slippage); nothing is held overnight. Stop and target take precedence over the close.
- Long and short: P&L = side x (exit fill - entry fill) x quantity - commissions; sizing is the mean-reversion funnel's (as many whole contracts as equity covers at full contract value, unlevered, compounding).
- Development backtests run on data physically truncated at the development end; the final session's trade is closed at the last development bar and flagged forced (not counted as completed).
- Sharpe: daily session-close mark-to-market returns over every trading day (flat days = 0), sqrt(252) annualization, rf = 0, idle cash earns 0.
- Look-ahead truncation test: 40 sampled configs x 3 cut points, failures: 0

## Futures data and execution

- Data: Databento GLBX.MDP3 ohlcv-1m continuous front month by volume (<ROOT>.v.0), built by scripts/build_futures_data.py.
- Rolls: difference back-adjusted at each instrument change (Databento rolls at 00:00 UTC; the 1-minute step there is taken as the roll spread). Point moves are preserved; pre-roll price levels are not real traded prices.
- Session: each root's day session only (src/data/futures.py SESSIONS: NYSE 09:30-16:00 NY for equity indexes, 09:00-14:30 NY for crude, 08:20-13:30 NY for gold, 08:20-15:00 NY for FX; sessions under 5% of normal volume are skipped), on NYSE trading days; overnight Globex bars are not traded or used in indicators.
- Sizing: whole contracts, as many as equity covers at full contract value (unadjusted price x multiplier) -- unlevered, compounding. Quantities in the trade log are contracts x multiplier.
- Costs: slippage in ticks per side (stops too) plus commission per contract per side, from the execution YAML; cost stress scales both.
- Rolls happen outside the day session (Databento rolls at 00:00 UTC) and every position is flat by the session close, so no trade straddles a roll; compression, box, stop and target are all point distances, so back-adjustment does not change them.

## Unresolved assumptions

- Drawdown limit -30% is reused from the SPY funnels; it was not separately approved for unlevered futures sizing.
- Drawdown is measured on daily session-close mark-to-market; intraday drawdown is deeper.
- rf = 0 and idle cash earns 0. Unlevered futures sit mostly in cash (T-bill interest in reality), so returns vs. a real account are understated in high-rate years while Sharpe vs. cash is unaffected by that choice.
- Variable cost stress scales per-contract commission and slippage ticks together.
- Trades are attributed to the year/window of their entry session; a position open at the development end is force-closed and excluded from completed-trade counts.
- Whole-contract granularity: at ~$1M equity the position is a handful of ES contracts, so position size steps with price; results are sensitive to starting equity at small sizes.
- All lengths (BB/KC length, NR-N, ATR(14), EMA(50), min squeeze bars, setup expiry) count bars of the config's timeframe and run across sessions over RTH bars only, so the overnight gap enters the first bars of each session: it widens sd and ATR there (bbkc) and can make the first bar's range look normal (nr). Runs and boxes themselves never span sessions.
- Bar data cannot order events inside a bar: a stop and a target in the same bar count as the stop, and a wick entry's own bar checks only the stop. Both choices are conservative; a target is never credited on the entry bar of a wick entry even when it was reached after the fill.
- Targets fill as if they were market orders at the target (with slippage), not as resting limits that may or may not be filled at the touch.
- Sizing ignores the stop distance (full equity per trade, as in the other families), so the box stop and the ATR stops change the exit, not the position size.
- Squeeze (BB inside KC) and NR-N are separate strategy lines with their own runs; a breakout is never compared across lines inside one run, so stage-6 dedup does not merge a squeeze config with an NR config that trades the same days.
