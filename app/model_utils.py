import os
import pickle
from typing import Any, List

import numpy as np


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
    predictions = model.predict(X)
    return np.asarray(predictions, dtype=float).ravel().tolist()
