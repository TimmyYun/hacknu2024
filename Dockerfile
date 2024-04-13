FROM python:3.11-bullseye as python-base

RUN apt-get update && apt-get upgrade -y

FROM python-base as main

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get install pip -y

RUN pip install -U pip setuptools && \
    pip install poetry

WORKDIR app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

COPY . entrypoint.sh ./

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
