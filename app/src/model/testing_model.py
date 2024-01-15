import json
import logging

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)
from sklearn.pipeline import Pipeline

from .utils import get_artifact_path

logger = logging.getLogger(__name__)


def print_metrics(predictions, target):
    metrics = {
        "RMSE": np.sqrt(mean_squared_error(predictions, target)),
        "MAPE": mean_absolute_percentage_error(predictions, target),
        "MAE": mean_absolute_error(predictions, target),
    }

    for metric, value in metrics.items():
        logger.debug(f"{metric}: {value}")

    with open(get_artifact_path() / "training_metrics.json", "w") as f:
        json.dump(metrics, f)


def test(
    pipeline: Pipeline,
    test_data: tuple[pd.DataFrame, pd.DataFrame],
):
    X, y = test_data
    test_predictions = pipeline.predict(X)
    test_target = y.values
    print_metrics(test_predictions, test_target)
