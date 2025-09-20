from __future__ import annotations

import argparse
from pathlib import Path
import pickle

import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train regression model and save as model.pkl"
    )
    parser.add_argument(
        "--data",
        required=True,
        help="Path to CSV dataset (expects YearsExperience, Salary)",
    )
    parser.add_argument("--target", default="Salary")
    parser.add_argument("--model-out", default="models/model.pkl")
    parser.add_argument("--metrics-out", default="models/metrics.json")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    # Clean possible unnamed index column
    for col in list(df.columns):
        if col.strip().lower().startswith("unnamed") or col.strip() == "":
            df = df.drop(columns=[col])

    feature_col = "YearsExperience"
    if feature_col not in df.columns or args.target not in df.columns:
        raise ValueError(
            "Dataset must contain 'YearsExperience' and target column (default 'Salary')"
        )

    y = df[args.target]
    X = df[[feature_col]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline([("scaler", StandardScaler()), ("reg", LinearRegression())])

    pipeline.fit(X_train, y_train)

    # Simple evaluation
    r2 = float(pipeline.score(X_test, y_test))

    out_path = Path(args.model_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"Saved model to {out_path}")

    metrics_path = Path(args.metrics_out)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, "w", encoding="utf-8") as mf:
        json.dump({"r2": r2, "samples_test": int(len(y_test))}, mf, indent=2)
    print(f"Saved metrics to {metrics_path} (r2={r2:.4f})")


if __name__ == "__main__":
    main()
