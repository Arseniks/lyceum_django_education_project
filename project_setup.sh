#!/bin/bash

set -ex

echo "Creating Virtual Environment"
python3 -m venv venv
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
python3 manage.py migrate
echo "Filling the database from a fixture"
python3 manage.py loaddata data.json
echo "Collecting static"
python3 manage.py collectstatic
echo "Running server"
python3 manage.py runserver
echo "Ending"
Exit
