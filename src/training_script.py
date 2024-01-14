import logging

from dataset.download_dataset import DataSet
from model.testing_model import test
from model.training_model import train

logger = logging.getLogger(__name__)

logger.debug("Loading and parsing the data")
data = DataSet()

logger.debug("Starting model training")
pipeline = train(training_data=data.train)

logger.debug("Evaluating the model")
test(pipeline=pipeline, test_data=data.test)
