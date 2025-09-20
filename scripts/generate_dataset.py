from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification


def group_seed(group_id: str) -> int:
    digest = hashlib.sha256(group_id.encode("utf-8")).hexdigest()
    # Take 8 hex chars -> 32-bit int
    return int(digest[:8], 16)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a unique synthetic dataset per group.")
    parser.add_argument("--group-id", required=True, help="Unique group identifier (e.g., userA_userB)")
    parser.add_argument("--samples", type=int, default=500)
    parser.add_argument("--features", type=int, default=6)
    parser.add_argument("--classes", type=int, default=3)
    parser.add_argument("--out", default="data/dataset_GROUP_DEMO.csv")
    args = parser.parse_args()

    rng_seed = group_seed(args.group_id)
    X, y = make_classification(
        n_samples=args.samples,
        n_features=args.features,
        n_informative=max(2, args.features // 2),
        n_redundant=max(0, args.features // 4),
        n_classes=args.classes,
        random_state=rng_seed,
    )

    columns = [f"f{i}" for i in range(args.features)]
    df = pd.DataFrame(X, columns=columns)
    df["target"] = y

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote dataset to {out_path}")


if __name__ == "__main__":
    main()


