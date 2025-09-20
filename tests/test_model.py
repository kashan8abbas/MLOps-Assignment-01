from pathlib import Path

import pandas as pd
import pytest

from app.model_utils import load_model, predict_with_model


@pytest.fixture(scope="session")
def demo_data() -> pd.DataFrame:
    return pd.read_csv("data/Salary_dataset.csv")


def test_model_file_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_model(str(tmp_path / "nope.pkl"))


def test_train_and_predict(demo_data: pd.DataFrame, tmp_path: Path):
    # Train quickly using script to ensure compatibility
    from subprocess import check_call

    model_path = tmp_path / "model.pkl"
    check_call(
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

    model = load_model(str(model_path))
    X = demo_data[["YearsExperience"]].head(5).values.tolist()
    preds = predict_with_model(model, X)
    assert len(preds) == 5
