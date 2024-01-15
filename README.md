# Machine Learning Model Training, Testing, and Serving API

This project provides a solution training, testing, and deploying the **Property-Friends Real State case** machine learning model.

## Prerequisites

Make sure you have the following components installed:

- Python 3.11
- Required Python libraries (see `requirements.txt`)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

ALso, make sure that you have uploaded the datasets to the `data` folder.

## Usage

The API provides the following endpoints:

- /docs: full documentation on a OpenAPI style
- /model-metrics
  - Exposes the training metrics obtained after the model training
- /predict
  - This is the only POST method, which requires the model's input parameters
- /test
  - runs the test dataset against the model Pipeline, outputting the model-training metrics
  - expects to find a CSV file named `test.csv` inside the data folder
- /train
  - Builds and execute the model training pipeline
  - Expects to find a CSV file named `train.csv` inside the data folder
- /token: Used for authentication, this dummy endpoint simulates an authentication process

## Running the API

To run this project, you should clone this repository and run

```bash
docker compose build
docker compose up  # or docker compose up -d
```

After that, the API will be launched at <http://localhost:8000> by default.
