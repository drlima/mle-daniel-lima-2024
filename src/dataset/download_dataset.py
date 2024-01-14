import logging
from pathlib import Path

import pandas as pd

from .models import Predictors, TargetColumn

logger = logging.getLogger(__name__)


class DataSchemaError(Exception):
    ...


class CSVDataSet:
    def load_data(self, file_name: str) -> pd.DataFrame:
        path = Path(__file__).parent.parent.parent / "data" / file_name
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
    predictors = [str(p) for p in Predictors]
    target = [str(t) for t in TargetColumn]
    db_connector = CSVDataSet()
    _train_data: pd.DataFrame
    _test_data: pd.DataFrame

    def __init__(self):
        self._load_train()
        self._load_test()

    @staticmethod
    def _all_columns_in_df(columns: list[str], data_frame: pd.DataFrame) -> bool:
        return all([col in data_frame.columns for col in columns])

    def _valid_schema(self, data: pd.DataFrame | None) -> bool:
        return self._all_columns_in_df(self.predictors, data) and self._all_columns_in_df(self.target, data)

    def _load_train(self):
        self._train_data = self.db_connector.load_data("train.csv")
        if self._train_data is not None and not self._valid_schema(self._train_data):
            raise DataSchemaError("Missing columns in training dataset")

    def _load_test(self):
        self._test_data = self.db_connector.load_data("test.csv")
        if self._test_data is not None and not self._valid_schema(self._test_data):
            raise DataSchemaError("Missing columns in test dataset")

    @property
    def train(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return self._train_data[self.predictors], self._train_data[self.target]

    @property
    def test(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        return self._test_data[self.predictors], self._test_data[self.target]
