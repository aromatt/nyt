#!/usr/bin/env bash

set -eu -o pipefail

proj=$(realpath $(dirname $0))
cd $proj

mkdir -p public/times

source env.sh

./fetch_leaderboard.py --format csv > "public/times/$(TZ='America/New_York' date +%Y-%m-%d).csv"
