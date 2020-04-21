#!/bin/bash

cd "${PWD}"
rm db.sqlite3
touch db.sqlite3
sleep 0.5
python3.8 manage.py makemigrations
sleep 0.5
python3.8 manage.py migrate
sleep 0.5
python3.8 manage.py createsuperuser
