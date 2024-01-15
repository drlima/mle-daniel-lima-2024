import logging
from pathlib import Path

import pandas as pd

from .data_models import Schema, get_predictors_names, get_target_name

logger = logging.getLogger(__name__)


class DataSchemaError(Exception):
    ...


class CSVDataSet:
    def load_data(self, file_name: str) -> pd.DataFrame:
        path = Path(__file__).parent.parent.parent.parent / "data" / file_name
        try:
            data = pd.read_csv(path)
        except FileNotFoundError:
            logger.exception(f"File {path} not found.")
        except pd.errors.EmptyDataError:
            logger.exception(f"No data in file {path}")
        except pd.errors.ParserError:
            logger.exception(f"Parser error in {path}")
        except Exception as e:
            logger.exception(e)
        return data


class DataSet:
    predictors = get_predictors_names()
    target = get_target_name()
    schema = Schema()
    db_connector = CSVDataSet()
    _train_data: pd.DataFrame
    _test_data: pd.DataFrame

    def __init__(self):
        self._load_train()
        self._load_test()

    def _load_train(self):
        self._train_data = self.db_connector.load_data("train.csv")
        if not self.schema.validate_schema(self._train_data):
            raise DataSchemaError("Missing columns in training dataset")

    def _load_test(self):
        self._test_data = self.db_connector.load_data("test.csv")
        if not self.schema.validate_schema(self._test_data):
            raise DataSchemaError("Missing columns in test dataset")

    @property
    def train(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return self._train_data[self.predictors], self._train_data[self.target]

    @property
    def test(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return self._test_data[self.predictors], self._test_data[self.target]
