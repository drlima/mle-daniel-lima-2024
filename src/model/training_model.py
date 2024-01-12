import pandas as pd
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline


def train(training_data: pd.DataFrame) -> Pipeline:
    train_cols = [col for col in training_data.columns if col not in ["id", "target"]]

    categorical_cols = ["type", "sector"]
    target = "price"

    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, categorical_cols),
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

    pipeline.fit(training_data[train_cols], training_data[target])
    return pipeline
