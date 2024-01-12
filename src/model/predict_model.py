import pandas as pd
from sklearn.pipeline import Pipeline


def predict(pipeline: Pipeline, predict_data: pd.Series) -> float:
    return pipeline.predict(predict_data.values)
