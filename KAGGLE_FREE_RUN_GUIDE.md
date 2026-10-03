# Kaggle Free Run Guide For Lab 16

Use this path when AWS/Oracle account verification is blocked.

## 1. Create The Kaggle Notebook

1. Open `https://www.kaggle.com/code`.
2. Click **New Notebook**.
3. In the notebook page, click **File** -> **Import Notebook** if available, then upload `kaggle_lab16_benchmark.ipynb`.
4. If Kaggle does not show **Import Notebook**, create a blank notebook, then use **File** -> **Upload Notebook** from the Kaggle notebooks page.

## 2. Add The Dataset

1. In the right sidebar, click **Add Data**.
2. Search for `creditcardfraud`.
3. Add the dataset named **Credit Card Fraud Detection** by `mlg-ulb`.
4. Confirm this file exists in the notebook:

```text
/kaggle/input/creditcardfraud/creditcard.csv
```

## 3. Run The Notebook

1. Open `kaggle_lab16_benchmark.ipynb`.
2. Make sure the accelerator is **None** or **CPU**.
3. Click **Run All**.
4. Wait until the benchmark cell prints all metrics.
5. The notebook writes:

```text
/kaggle/working/benchmark_result.json
```

## 4. Evidence To Capture

Take screenshots of:

- The benchmark output cell with AUC-ROC, Accuracy, F1, Precision, Recall, training time, and inference speed.
- The JSON output cell showing `benchmark_result.json`.
- The resource evidence cell showing CPU count and memory info.
- The Kaggle notebook sidebar or settings showing CPU/no accelerator.

Download and submit:

- `benchmark_result.json`
- `kaggle_lab16_benchmark.ipynb`
- `benchmark.py`

## 5. Suggested Report

Fill in the values from the notebook:

```text
Because AWS account verification and Oracle Cloud sign-up were blocked, I completed the CPU benchmark on Kaggle Notebook, a free managed cloud notebook environment. I used the Credit Card Fraud Detection dataset with 284,807 transactions and trained a LightGBM binary classifier. The benchmark measured data loading time, training time, AUC-ROC, Accuracy, F1-score, Precision, Recall, single-row inference latency, and 1000-row inference throughput. The model achieved AUC-ROC = <AUC>, Accuracy = <ACC>, F1 = <F1>, Precision = <PRECISION>, and Recall = <RECALL>. Training took <TRAINING_TIME> seconds. Single-row inference latency was <LATENCY> ms and 1000-row throughput was <THROUGHPUT> rows/second. The result was saved to benchmark_result.json. This path used CPU only, no GPU, and no paid cloud resources.
```

