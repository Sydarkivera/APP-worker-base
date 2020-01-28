#!/bin/sh

# wait for PSQL server to start
# sleep 10

# cd myproject
# prepare init migration
python /code/manage.py makemigrations
python /code/manage.py makemigrations api
# migrate db, so we have the latest db schema
python /code/manage.py migrate
# populate database with default data
# python populate_database.py

gunicorn --chdir /code/ config.wsgi:application -w 2 -b :80
