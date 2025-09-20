import os
from pathlib import Path

import pytest
from flask import Flask

from app import create_app


@pytest.fixture(scope="session")
def app_with_model(tmp_path_factory: pytest.TempPathFactory) -> Flask:
    # Train a temporary model to use in tests
    tmp_dir = tmp_path_factory.mktemp("model")
    model_path = tmp_dir / "model.pkl"

    import subprocess

    subprocess.check_call(
        [
            "python",
            "scripts/train_model.py",
            "--data",
            "data/Salary_dataset.csv",
            "--target",
            "Salary",
            "--model-out",
            str(model_path),
        ]
    )

    os.environ["MODEL_PATH"] = str(model_path)
    app = create_app()
    app.config.update({"TESTING": True})
    return app


def test_health(app_with_model: Flask):
    client = app_with_model.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_predict_list_of_numbers(app_with_model: Flask):
    client = app_with_model.test_client()
    payload = {"instances": [1.2, 3.0, 10.6]}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "predictions" in data
    assert len(data["predictions"]) == 3


def test_predict_list_of_dicts(app_with_model: Flask):
    client = app_with_model.test_client()
    payload = {"instances": [{"YearsExperience": 1.2}, {"YearsExperience": 10.6}]}
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert "predictions" in data
    assert len(data["predictions"]) == 2


def test_predict_missing_instances(app_with_model: Flask):
    client = app_with_model.test_client()
    resp = client.post("/predict", json={})
    assert resp.status_code == 400
    assert "error" in resp.get_json()
