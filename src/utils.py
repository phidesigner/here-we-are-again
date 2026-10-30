"""Shared utilities for reading and saving data and models.

Inputs: File paths, pandas DataFrames, and trained models.
Outputs: Loaded data or models, and saved files.
Used by: Data loading, training, and inference modules.
Why: Keep file operations consistent across the pipeline.
"""

from pathlib import Path

import joblib
import pandas as pd