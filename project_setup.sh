#!/bin/bash

set -ex

echo "Creating Virtual Environment"
python -m venv venv
echo "Activating Virtual Environment"
source venv/bin/activate
echo "Switching git branch"
git checkout $GIT_BRANCH
echo "Creating .env, don't forget to change values"
cp .env.template .env
echo "Installing dependencies"
pip install -r requirements/requirements.txt
pip install -r requirements/requirements_dev.txt
pip install -r requirements/requirements_test.txt
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
