import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)
from sklearn.pipeline import Pipeline


def print_metrics(predictions, target):
    print("RMSE: ", np.sqrt(mean_squared_error(predictions, target)))
    print("MAPE: ", mean_absolute_percentage_error(predictions, target))
    print("MAE : ", mean_absolute_error(predictions, target))


def test(
    pipeline: Pipeline,
    test_data: pd.DataFrame,
    target_column: str,
    train_cols: list[str],
):
    test_predictions = pipeline.predict(test_data[train_cols])
    test_target = test_data[target_column].values
    print_metrics(test_predictions, test_target)
