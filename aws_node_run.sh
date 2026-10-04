#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import lightgbm, sklearn, pandas, numpy
print("ml-env-ok")
PY

mkdir -p ~/ml-benchmark
~/.local/bin/kaggle datasets download -d mlg-ulb/creditcardfraud --unzip -p ~/ml-benchmark/
python3 ~/benchmark.py --output ~/benchmark_result.json
cat ~/benchmark_result.json

echo "RESOURCE_EVIDENCE_START"
python3 - <<'PY'
import multiprocessing
print("CPU count:", multiprocessing.cpu_count())
PY
free -h
ip -s link
echo "RESOURCE_EVIDENCE_END"
