#!/usr/bin/env python3
"""
LightGBM benchmark for Lab 16.

Expected dataset:
  ~/ml-benchmark/creditcard.csv

Outputs:
  benchmark_result.json
"""

import argparse
import json
import platform
import time
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


def seconds_since(start_time):
    return round(time.perf_counter() - start_time, 6)


def milliseconds_since(start_time):
    return round((time.perf_counter() - start_time) * 1000, 6)


def print_metric(name, value):
    print(f"{name:<36} {value}")


def main():
    parser = argparse.ArgumentParser(description="Run the Lab 16 LightGBM benchmark.")
    parser.add_argument(
        "--data",
        default=str(Path.home() / "ml-benchmark" / "creditcard.csv"),
        help="Path to creditcard.csv",
    )
    parser.add_argument(
        "--output",
        default="benchmark_result.json",
        help="Path for the benchmark JSON output",
    )
    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducible train/test split",
    )
    args = parser.parse_args()

    data_path = Path(args.data).expanduser()
    output_path = Path(args.output).expanduser()

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {data_path}. Download it with Kaggle first."
        )

    print("Lab 16 LightGBM Credit Card Fraud Benchmark")
    print(f"Dataset: {data_path}")
    print()

    load_started = time.perf_counter()
    data = pd.read_csv(data_path)
    load_time_seconds = seconds_since(load_started)

    expected_columns = {"Class", "Amount", "Time"}
    missing_columns = sorted(expected_columns - set(data.columns))
    if missing_columns:
        raise ValueError(f"Dataset is missing expected columns: {missing_columns}")

    y = data["Class"].astype(int)
    x = data.drop(columns=["Class"])

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=args.random_state,
    )

    positive_count = int(y_train.sum())
    negative_count = int(len(y_train) - positive_count)
    scale_pos_weight = negative_count / positive_count

    model = lgb.LGBMClassifier(
        objective="binary",
        boosting_type="gbdt",
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_pos_weight,
        random_state=args.random_state,
        n_jobs=-1,
    )

    training_started = time.perf_counter()
    model.fit(
        x_train,
        y_train,
        eval_set=[(x_test, y_test)],
        eval_metric="auc",
        callbacks=[lgb.early_stopping(30, verbose=False)],
    )
    training_time_seconds = seconds_since(training_started)

    prediction_started = time.perf_counter()
    y_probability = model.predict_proba(x_test)[:, 1]
    batch_prediction_time_seconds = seconds_since(prediction_started)
    precisions, recalls, thresholds = precision_recall_curve(y_test, y_probability)
    f1_scores = 2 * precisions * recalls / (precisions + recalls + 1e-12)
    best_index = int(np.nanargmax(f1_scores[:-1]))
    best_threshold = float(thresholds[best_index])
    y_predicted = (y_probability >= best_threshold).astype(int)

    one_row = x_test.iloc[[0]]
    latency_started = time.perf_counter()
    model.predict_proba(one_row)
    single_row_latency_ms = milliseconds_since(latency_started)

    thousand_rows = x_test.iloc[:1000]
    throughput_started = time.perf_counter()
    model.predict_proba(thousand_rows)
    thousand_row_time_seconds = seconds_since(throughput_started)
    rows_per_second = round(len(thousand_rows) / thousand_row_time_seconds, 3)

    metrics = {
        "decision_threshold": round(best_threshold, 6),
        "dataset_path": str(data_path),
        "rows": int(len(data)),
        "features": int(x.shape[1]),
        "fraud_rows": int(y.sum()),
        "fraud_rate": round(float(y.mean()), 8),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "load_time_seconds": load_time_seconds,
        "training_time_seconds": training_time_seconds,
        "best_iteration": int(model.best_iteration_ or model.n_estimators),
        "auc_roc": round(float(roc_auc_score(y_test, y_probability)), 6),
        "accuracy": round(float(accuracy_score(y_test, y_predicted)), 6),
        "f1_score": round(float(f1_score(y_test, y_predicted, zero_division=0)), 6),
        "precision": round(
            float(precision_score(y_test, y_predicted, zero_division=0)), 6
        ),
        "recall": round(float(recall_score(y_test, y_predicted, zero_division=0)), 6),
        "single_row_inference_latency_ms": single_row_latency_ms,
        "thousand_row_inference_time_seconds": thousand_row_time_seconds,
        "inference_throughput_rows_per_second": rows_per_second,
        "batch_prediction_time_seconds": batch_prediction_time_seconds,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }

    output_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")

    print("Benchmark results")
    print("-" * 60)
    print_metric("Rows", metrics["rows"])
    print_metric("Fraud rows", metrics["fraud_rows"])
    print_metric("Fraud rate", metrics["fraud_rate"])
    print_metric("Load data time (seconds)", metrics["load_time_seconds"])
    print_metric("Training time (seconds)", metrics["training_time_seconds"])
    print_metric("Best iteration", metrics["best_iteration"])
    print_metric("AUC-ROC", metrics["auc_roc"])
    print_metric("Accuracy", metrics["accuracy"])
    print_metric("F1-score", metrics["f1_score"])
    print_metric("Precision", metrics["precision"])
    print_metric("Recall", metrics["recall"])
    print_metric(
        "Inference latency, 1 row (ms)",
        metrics["single_row_inference_latency_ms"],
    )
    print_metric(
        "Inference throughput, 1000 rows/s",
        metrics["inference_throughput_rows_per_second"],
    )
    print("-" * 60)
    print(f"Saved JSON result to: {output_path}")


if __name__ == "__main__":
    main()
