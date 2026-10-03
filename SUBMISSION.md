# Lab 16 Submission - Cloud AI CPU Benchmark

## Execution Environment

- Platform: Kaggle Notebook CPU
- Accelerator: None
- CPU count: 4
- Memory: 32,869,444 kB total
- Dataset: Credit Card Fraud Detection (`mlg-ulb/creditcardfraud`)
- Dataset path: `/kaggle/input/datasets/mlg-ulb/creditcardfraud/creditcard.csv`
- Output file: `benchmark_result.json`

AWS account verification and Oracle Cloud sign-up were blocked during setup, so the benchmark was completed on Kaggle Notebook, a free managed cloud notebook environment. This preserves the core Lab 16 CPU benchmark objective without using GPU or paid cloud resources.

## Benchmark Results

| Metric | Result |
|---|---:|
| Rows | 284,807 |
| Fraud rows | 492 |
| Fraud rate | 0.00172749 |
| Load data time | 2.220287 seconds |
| Training time | 1.504332 seconds |
| Best iteration | 1 |
| AUC-ROC | 0.922938 |
| Accuracy | 0.998122 |
| F1-score | 0.60223 |
| Precision | 0.473684 |
| Recall | 0.826531 |
| Inference latency, 1 row | 1.845587 ms |
| Inference throughput, 1000 rows | 438,788.943 rows/second |

## Submitted Files

- `benchmark.py`: standalone benchmark script for the CPU LightGBM workflow.
- `kaggle_lab16_benchmark.ipynb`: Kaggle notebook used for the free cloud run.
- `benchmark_result.json`: measured benchmark output.
- `LAB16_KAGGLE_REPORT.md`: short written report.
- `KAGGLE_FREE_RUN_GUIDE.md`: reproducible Kaggle run guide.

## Evidence Screenshots

The captured screenshots show:

- LightGBM benchmark output with all required metrics.
- `benchmark_result.json` printed from `/kaggle/working`.
- Resource evidence with 4 CPU cores and memory information.
- Kaggle notebook settings showing accelerator set to `None`.

## Short Report

Because AWS account verification and Oracle Cloud sign-up were blocked, I completed the CPU benchmark on Kaggle Notebook, a free managed cloud notebook environment. I used the Credit Card Fraud Detection dataset with 284,807 transactions and trained a LightGBM binary classifier to detect fraudulent transactions. The benchmark measured data loading time, training time, AUC-ROC, Accuracy, F1-score, Precision, Recall, single-row inference latency, and 1000-row inference throughput. The model achieved AUC-ROC = 0.922938, Accuracy = 0.998122, F1-score = 0.60223, Precision = 0.473684, and Recall = 0.826531. Training took 1.504332 seconds, single-row inference latency was 1.845587 ms, and 1000-row throughput was 438,788.943 rows/second. The result was saved to `benchmark_result.json`. This path used CPU only, no GPU, and no paid cloud resources.
