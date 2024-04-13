#!/bin/bash

poetry run python hacknu/manage.py makemigrations core
poetry run python hacknu/manage.py migrate core
poetry run python hacknu/manage.py makemigrations
poetry run python hacknu/manage.py migrate

poetry run python hacknu/manage.py runserver 0.0.0.0:8000

exec "$@"
