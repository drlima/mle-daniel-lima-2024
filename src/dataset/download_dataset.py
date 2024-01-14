import logging
from pathlib import Path

import pandas as pd
from strenum import StrEnum

logger = logging.getLogger(__name__)


class DataSchemaError(Exception):
    ...


class Predictors(StrEnum):
    TYPE = "type"
    SECTOR = "sector"
    NET_USABLE_AREA = "net_usable_area"
    NET_AREA = "net_area"
    N_ROOMS = "n_rooms"
    N_BATHROOM = "n_bathroom"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"


class TargetColumn(StrEnum):
    PRICE = "price"


class CSVDataSet:
    def load_data(self, path: Path) -> pd.DataFrame | None:
        try:
            data = pd.read_csv(path)
            return data
        except FileNotFoundError:
            logger.error(f"File {path} not found.")
        except pd.errors.EmptyDataError:
            logger.error(f"No data in file {path}")
        except pd.errors.ParserError:
            logger.error(f"Parser error in {path}")
        except Exception as e:
            logger.error(e)
        return None


class DataSet:
    predictors = Predictors
    target = TargetColumn
    data_uri: Path
    con = CSVDataSet()
    _train_data: pd.DataFrame | None
    _test_data: pd.DataFrame | None

    def __init__(self, data_uri: Path) -> None:
        self.data_uri = data_uri

    @staticmethod
    def _columns_in_df(columns: Predictors | TargetColumn, data_frame: pd.DataFrame):
        if not all([col in data_frame.columns for col in columns]):
            raise DataSchemaError()

    def _data_schema_validator(self, data: pd.DataFrame | None):
        if data is not None:
            self._columns_in_df(self.predictors, data)  # type: ignore[arg-type]
            self._columns_in_df(self.target, data)  # type: ignore[arg-type]

    def load_data(self):
        """
        Loads the train and test data into pandas DataFrames
        """
        self._train_data = self.con.load_data(self.data_uri / "train.csv")
        try:
            self._data_schema_validator(self._train_data)
        except DataSchemaError:
            logger.error("Missing columns in training dataset")
            self._train_data = None

        self._test_data = self.con.load_data(self.data_uri / "test.csv")
        try:
            self._data_schema_validator(self._test_data)
        except DataSchemaError:
            logger.error("Missing columns in training dataset")
            self._test_data = None

    @property
    def train(self) -> pd.DataFrame:
        if self._train_data is None:
            return pd.DataFrame()
        return self._train_data.copy()

    @property
    def test(self) -> pd.DataFrame:
        if self._test_data is None:
            return pd.DataFrame()
        return self._test_data.copy()
