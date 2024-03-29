import logging
import pickle

import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

from app.config import get_settings
from app.src.dataset import CATEGORICAL_PREDICTORS
from .utils import get_artifact_path

logger = logging.getLogger(__name__)

MODEL_SETTINGS = get_settings()


def train(training_data: tuple[pd.DataFrame, pd.DataFrame]) -> Pipeline:
    logger.info("Starting model training.")
    X, y = training_data

    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, [c.name for c in CATEGORICAL_PREDICTORS]),
        ],
    )

    steps = [
        ("preprocessor", preprocessor),
        (
            "model",
            GradientBoostingRegressor(
                **{
                    "learning_rate": MODEL_SETTINGS.learning_rate,
                    "n_estimators": MODEL_SETTINGS.n_estimators,
                    "max_depth": MODEL_SETTINGS.max_depth,
                    "loss": MODEL_SETTINGS.loss,
                }
            ),
        ),
    ]

    pipeline = Pipeline(steps)

    pipeline.fit(X, y)
    logger.info("Finished model training.")

    with open(get_artifact_path() / "model_pipeline.pkl", "wb") as f:
        pickle.dump(pipeline, f)
    return pipeline
