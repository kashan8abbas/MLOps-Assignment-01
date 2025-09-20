import os
import pickle
from typing import Any, List

import numpy as np
import pandas as pd


def load_model(model_path: str | None = None) -> Any:
    path = model_path or os.environ.get("MODEL_PATH", "models/model.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}")
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model


def predict_with_model(
    model: Any, instances: List[List[float]] | List[float] | np.ndarray
) -> List[float]:
    # Support either list of single-feature values or list of lists
    if (
        isinstance(instances, list)
        and len(instances) > 0
        and not isinstance(instances[0], (list, tuple, np.ndarray))
    ):
        X = np.asarray([[float(v)] for v in instances], dtype=float)
    else:
        X = np.asarray(instances, dtype=float)

    # If the model (or a step in a pipeline) was fitted with feature names
    # (pandas DataFrame), passing a DataFrame with the same column names
    # avoids the sklearn warning:
    # "X does not have valid feature names, but StandardScaler was fitted
    #  with feature names"
    feature_names = None
    # Top-level estimator with feature_names_in_
    if hasattr(model, "feature_names_in_"):
        feature_names = list(getattr(model, "feature_names_in_"))
    else:
        # If this is a Pipeline, check its steps for feature_names_in_
        if hasattr(model, "named_steps"):
            for step in model.named_steps.values():
                if hasattr(step, "feature_names_in_"):
                    feature_names = list(getattr(step, "feature_names_in_"))
                    break

    if feature_names is not None:
        try:
            X = pd.DataFrame(X, columns=feature_names)
        except Exception:
            # If shapes don't match or conversion fails, fall back to numpy
            X = np.asarray(X, dtype=float)
    predictions = model.predict(X)
    return np.asarray(predictions, dtype=float).ravel().tolist()
