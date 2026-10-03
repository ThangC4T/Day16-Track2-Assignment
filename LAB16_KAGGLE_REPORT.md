# Lab 16 Report - Kaggle CPU Benchmark

Because AWS account verification and Oracle Cloud sign-up were blocked, I completed the CPU benchmark on Kaggle Notebook, a free managed cloud notebook environment. I used the Credit Card Fraud Detection dataset with 284,807 transactions and trained a LightGBM binary classifier to detect fraudulent transactions. The benchmark measured data loading time, training time, classification metrics, single-row inference latency, and 1000-row inference throughput.

The dataset contained 492 fraud rows, with a fraud rate of 0.00172749. Data loading took 2.220287 seconds and model training took 1.504332 seconds. The model achieved AUC-ROC = 0.922938, Accuracy = 0.998122, F1-score = 0.60223, Precision = 0.473684, and Recall = 0.826531. Single-row inference latency was 1.845587 ms, and inference throughput for 1000 rows was 438,788.943 rows/second. The benchmark result was saved to `benchmark_result.json`. The run used CPU only on Kaggle Notebook with 4 CPU cores and about 32 GB RAM, with no GPU and no paid cloud resources.

