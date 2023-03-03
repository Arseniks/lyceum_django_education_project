#!/bin/bash

set -ex

cd lyceum_django_education_project || exit
echo "Creating .env, don't forget to change values"
cp .env.template .env
echo "Creating Virtual Environment"
python -m venv venv
echo "Activating Virtual Environment"
.\env\Scripts\activate
echo "Installing dependencies"
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -r requirements_test.txt
echo "Installing migrations"
python manage.py migrate
echo "Filling the database from a fixture"
python manage.py loaddata data.json
echo "Collecting static"
python manage.py collectstatic
echo "Running server"
python manage.py runserver
echo "Ending"
Exit
