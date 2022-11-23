#!/usr/bin/env bash

set -eu -o pipefail

proj=$(realpath $(dirname $0))
cd $proj

mkdir -p public/times

source env.sh

export TZ='America/New_York'

HOUR=$(date +%H)
DAY_OF_WEEK=$(date +%u)

# Cut-off time is different for weekends
if (("${DAY_OF_WEEK}" >= 6)); then
  CUTOFF_HOUR=18
else
  CUTOFF_HOUR=22
fi

if (("${HOUR}" >= ${CUTOFF_HOUR})); then
  PUZZLE_DATE=$(date --date tomorrow +%Y-%m-%d)
else
  PUZZLE_DATE=$(date +%Y-%m-%d)
fi

echo "[$(date -u)] HOUR $HOUR DAY_OF_WEEK $DAY_OF_WEEK CUTOFF_HOUR $CUTOFF_HOUR PUZZLE_DATE $PUZZLE_DATE"

./fetch_leaderboard.py --format csv > "public/times/${PUZZLE_DATE}.csv"
