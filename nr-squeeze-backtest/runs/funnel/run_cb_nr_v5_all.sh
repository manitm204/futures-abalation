#!/usr/bin/env bash
cd "$(dirname "$0")/../.."
for t in 15m 5m; do for s in es nq rty ym gc cl; do
  [ "$s$t" = "es5m" ] && continue
  ./runs/funnel/run_cb_nr_v5.sh $s $t > runs/funnel/cb_nr_${s}_v5_${t}.log 2> runs/funnel/cb_nr_${s}_v5_${t}.err || echo "FAILED $s $t"
done; done; echo ALLDONE
