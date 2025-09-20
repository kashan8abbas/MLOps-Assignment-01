from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, List

from flask import Blueprint, jsonify, request

from .model_utils import load_model, predict_with_model


bp = Blueprint("app", __name__)


@dataclass
class AppState:
    model: Any | None = None


STATE = AppState()


@bp.before_app_request
def _ensure_model_loaded() -> None:
    if STATE.model is None:
        model_path = os.environ.get("MODEL_PATH", "models/model.pkl")
        STATE.model = load_model(model_path)


@bp.get("/health")
def health() -> Any:
    return jsonify({"status": "ok"})


@bp.get("/")
def index() -> Any:
    return jsonify(
        {
            "message": "Flask ML service is running",
            "endpoints": {
                "GET /health": "health check",
                "POST /predict": "send JSON with 'instances' to get predictions",
            },
        }
    )


@bp.post("/predict")
def predict() -> Any:
    payload = request.get_json(silent=True) or {}
    instances_field = payload.get("instances")
    if instances_field is None:
        return jsonify({"error": "Missing 'instances' in JSON body"}), 400

    # Accept: list of numbers (YearsExperience), or list of dicts with 'YearsExperience', or list of lists [[x], ...]
    instances: List[List[float]] | List[float]
    if (
        isinstance(instances_field, list)
        and len(instances_field) > 0
        and isinstance(instances_field[0], dict)
    ):
        instances = [float(row.get("YearsExperience"))
                     for row in instances_field]
    elif (
        isinstance(instances_field, list)
        and len(instances_field) > 0
        and not isinstance(instances_field[0], (list, tuple))
    ):
        instances = [float(x) for x in instances_field]
    else:
        instances = [[float(x) for x in row] for row in instances_field]

    if STATE.model is None:
        model_path = os.environ.get("MODEL_PATH", "models/model.pkl")
        STATE.model = load_model(model_path)

    preds = predict_with_model(STATE.model, instances)
    return jsonify({"predictions": preds})


# hello this is the 2nd change in dev and going to merge it with master
