ARG IMAGE_TAG=3.11.1-slim-bullseye

FROM python:$IMAGE_TAG as base

ARG PYTHONUSERBASE=/tmp/requirements

RUN apt-get update && apt-get install -y libpq-dev libffi-dev libssl-dev libcurl4-openssl-dev gcc

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --user --no-deps --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt

FROM python:$IMAGE_TAG

ARG RELEASE=latest

ENV RELEASE ${RELEASE}

COPY --from=base /tmp/requirements/ /usr/local/

RUN useradd -M apiuser
RUN apt-get update && apt-get install -y \
    libpq5 \
    libffi7 \
    libssl1.1 \
    libcurl4 \
    &&  rm -rf /var/lib/apt/lists/*

USER apiuser

WORKDIR /app

COPY --chown=apiuser:apiuser ./app ./app
COPY --chown=apiuser:apiuser ./artifacts  ./artifacts
COPY --chown=apiuser:apiuser ./data  ./data


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
