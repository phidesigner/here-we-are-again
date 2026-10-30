"""Shared utilities for reading and saving data and models.

Inputs: File paths, pandas DataFrames, and trained models.
Outputs: Loaded data or models, and saved files.
Used by: Data loading, training, and inference modules.
Why: Keep file operations consistent across the pipeline.
"""

from pathlib import Path

import joblib
import pandas as pd


def load_csv(filepath: Path) -> pd.DataFrame:
    """Read a CSV file.

    Inputs: Path to a CSV file.
    Outputs: DataFrame containing the loaded data.
    Why: Provide consistent CSV loading and clear errors.
    """
    # TODO: replace print with logging (Session 10)
    print(f"Loading CSV: {filepath}")

    if not filepath.is_file():
        raise FileNotFoundError(
            f"CSV file not found: {filepath}. Check the input path."
        )

    return pd.read_csv(filepath)


def save_csv(df: pd.DataFrame, filepath: Path) -> None:
    """Save a DataFrame as a CSV file.

    Inputs: DataFrame and destination path.
    Outputs: CSV file saved to disk.
    Why: Save data consistently without unnecessary index columns.
    """
    # TODO: replace print with logging (Session 10)
    print(f"Saving CSV: {filepath}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)


def save_model(model: object, filepath: Path) -> None:
    """Save a trained model to disk.

    Inputs: Trained model and destination path.
    Outputs: Serialized model file.
    Why: Preserve trained models for reuse and inference.
    """
    # TODO: replace print with logging (Session 10)
    print(f"Saving model: {filepath}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, filepath)


def load_model(filepath: Path) -> object:
    """Load a previously saved model.

    Inputs: Path to a saved model file.
    Outputs: Reloaded model object.
    Why: Reuse trained models without retraining.
    """
    # TODO: replace print with logging (Session 10)
    print(f"Loading model: {filepath}")

    if not filepath.is_file():
        raise FileNotFoundError(
            f"Model file not found: {filepath}. Check the model path."
        )

    return joblib.load(filepath)
