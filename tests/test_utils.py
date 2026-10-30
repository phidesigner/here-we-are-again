"""Test reusable data and model file operations.

Inputs: Synthetic data, temporary paths, and test models.
Outputs: Assertions verifying file operations.
Used by: pytest.
Why: Ensure shared utilities work before other modules depend on them.
"""

import pandas as pd
import pytest
from sklearn.dummy import DummyClassifier

from src.utils import load_csv, load_model, save_csv, save_model


def _make_df() -> pd.DataFrame:
    """Create a small, predictable dataset for testing."""
    return pd.DataFrame({
        "feature": [0, 1, 2, 3, 4, 5],
        "target": [0, 0, 0, 1, 1, 1],
    })


def test_unit_csv_round_trip(tmp_path):
    """Saving and reloading a CSV must preserve the original data."""
    original = _make_df()
    filepath = tmp_path / "nested" / "sample.csv"

    save_csv(original, filepath)
    reloaded = load_csv(filepath)

    assert filepath.is_file()
    pd.testing.assert_frame_equal(reloaded, original)


def test_unit_load_csv_missing_file(tmp_path):
    """Loading a missing CSV must raise FileNotFoundError."""
    filepath = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(filepath)


def test_integration_model_round_trip(tmp_path):
    """A reloaded model must produce the same predictions."""
    df = _make_df()
    X = df.drop(columns="target")
    y = df["target"]

    model = DummyClassifier(strategy="most_frequent")
    model.fit(X, y)

    filepath = tmp_path / "nested" / "model.joblib"

    save_model(model, filepath)
    reloaded = load_model(filepath)

    assert filepath.is_file()
    assert reloaded.predict(X).tolist() == model.predict(X).tolist()
