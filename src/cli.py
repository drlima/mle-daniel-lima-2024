from pathlib import Path

from dataset.download_dataset import DataSet, Predictors, TargetColumn
from model.testing_model import test
from model.training_model import train

DATA_PATH = Path(__file__).parent.parent / "data"

data = DataSet(data_uri=DATA_PATH)
data.load_data()

pipeline, train_cols = train(training_data=data.train)
test(pipeline=pipeline, test_data=data.test, target_column=TargetColumn.PRICE, train_cols=[str(p) for p in Predictors])
