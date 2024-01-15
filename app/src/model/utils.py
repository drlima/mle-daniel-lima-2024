import os
from pathlib import Path


def get_artifact_path() -> Path:
    MODEL_PATH = Path(__file__).parent.parent.parent.parent / "artifacts"
    os.makedirs(MODEL_PATH, exist_ok=True)
    return MODEL_PATH
