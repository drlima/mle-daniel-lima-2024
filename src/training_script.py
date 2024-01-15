import logging

from model import Model

logger = logging.getLogger(__name__)

model = Model()

logger.debug("Loading and parsing the data")
logger.debug("Starting model training")
pipeline = model.train()

logger.debug("Evaluating the model")
model.test()
