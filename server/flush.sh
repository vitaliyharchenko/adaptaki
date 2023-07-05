#!/bin/bash

echo -e "\n>>> Resetting the database"
./manage.py reset_db --noinput

echo -e "\n>>> Running migrations"
./manage.py migrate

echo -e "\n>>> Creating new superuser 'admin'"
./manage.py createsuperuser \
   --phone +79826469454

echo -e "\n>>> Database restore finished."