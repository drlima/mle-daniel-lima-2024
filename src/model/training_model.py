import logging
import pickle  # nosec

import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

from dataset import Predictors

from .utils import get_artifact_path

logger = logging.getLogger(__name__)


def train(training_data: tuple[pd.DataFrame, pd.DataFrame]) -> Pipeline:
    logger.info("Starting model training.")
    X, y = training_data

    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, Predictors.categorical()),
        ],
    )

    steps = [
        ("preprocessor", preprocessor),
        (
            "model",
            GradientBoostingRegressor(
                **{
                    "learning_rate": 0.01,
                    "n_estimators": 300,
                    "max_depth": 5,
                    "loss": "absolute_error",
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
