from pathlib import Path


def get_artifact_path() -> Path:
    MODEL_PATH = Path(__file__).parent.parent.parent.parent / "artifacts"
    MODEL_PATH.mkdir(parents=True, exist_ok=True)
    return MODEL_PATH
