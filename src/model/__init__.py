import json
import pickle

import pandas as pd
from sklearn.pipeline import Pipeline

from dataset import DataSet

from .testing_model import test
from .training_model import train
from .utils import get_artifact_path


class Model:
    _pipeline: Pipeline
    _model_metrics: dict[str, float]
    _data: DataSet

    def __init__(self, train_test: bool = False, load_model: bool = False):
        self._data = DataSet()
        if train_test:
            self.train()
            self.test()
        if load_model:
            self.load_model()

    def train(self):
        self._pipeline = train(training_data=self._data.train)

    def test(self):
        if self._pipeline is None:
            self.load_model()
        test(pipeline=self._pipeline, test_data=self._data.test)

    def load_model(self):
        artifact_path = get_artifact_path()
        # load model pipeline
        with open(artifact_path / "model_pipeline.pkl", "rb") as f:
            self._pipeline = pickle.load(f)

        # load training metrics
        with open(artifact_path / "training_metrics.json") as f:
            self._model_metrics = json.load(f)

    def predict(self, pipeline: Pipeline, predict_data: pd.Series) -> float:
        return pipeline.predict(predict_data.values)
