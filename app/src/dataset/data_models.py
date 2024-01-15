from functools import cache

import pandas as pd


class Column:
    def __init__(self, name: str, dtype: type):
        self.name = name
        self.dtype = dtype


CATEGORICAL_PREDICTORS: list[Column] = [
    Column(name="type", dtype=str),
    Column(name="sector", dtype=str),
]

PREDICTORS: list[Column] = [
    *CATEGORICAL_PREDICTORS,
    Column(name="net_usable_area", dtype=float),
    Column(name="net_area", dtype=float),
    Column(name="n_rooms", dtype=float),
    Column(name="n_bathroom", dtype=float),
    Column(name="latitude", dtype=float),
    Column(name="longitude", dtype=float),
]


TARGET_COLUMN = Column(name="price", dtype=float)


DATASET_COLUMNS = PREDICTORS + [TARGET_COLUMN]


@cache
def get_predictors_names() -> list[str]:
    return [p.name for p in PREDICTORS]


def get_target_name() -> str:
    return TARGET_COLUMN.name


class Schema:
    schema = {c.name: c.dtype for c in DATASET_COLUMNS}

    def validate_schema(self, data: pd.DataFrame) -> bool:
        return all([col in self.schema for col in data.columns])
