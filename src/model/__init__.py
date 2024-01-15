import json
import pickle

import pandas as pd
from sklearn.pipeline import Pipeline

from src.dataset import DataSet

from .testing_model import test
from .training_model import train
from .utils import get_artifact_path


class Model:
    _pipeline: Pipeline | None = None
    _model_metrics: dict[str, float]
    _data: DataSet | None = None

    def __init__(self, load_data: bool = False, train_test: bool = False, load_model: bool = False):
        if load_data:
            self._data = DataSet()
        if train_test:
            self.train()
            self.test()
        if load_model:
            self.load_model()

    def _load_data(self):
        self._data = DataSet()

    def train(self):
        if self._data is None:
            self._load_data()
        self._pipeline = train(training_data=self._data.train)

    def test(self):
        if self._pipeline is None:
            self.load_model()
        if self._data is None:
            self._load_data()
        test(pipeline=self._pipeline, test_data=self._data.test)
        self.load_metrics()

    def load_model(self):
        # load model pipeline
        with open(get_artifact_path() / "model_pipeline.pkl", "rb") as f:
            self._pipeline = pickle.load(f)

    def load_metrics(self):
        # load training metrics
        with open(get_artifact_path() / "training_metrics.json") as f:
            self._model_metrics = json.load(f)

    @property
    def model_metrics(self) -> dict[str, float]:
        return self._model_metrics

    def predict(
        self,
        **kwargs,
    ) -> float:
        if self._pipeline is None:
            self.load_model()
        input_data = pd.DataFrame(data=kwargs, index=[0])
        return self._pipeline.predict(input_data)  # type: ignore[union-attr]
