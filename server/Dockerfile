# Tutorial by
# https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

# Fetching official base image for python
FROM python:3.11.4-slim-buster

# Upgrape all the packages
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get -y install build-essential gcc python3-dev python3-pip
RUN apt install -y netcat

# Setting up the work directory
WORKDIR /code

# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1

# Flushing out python buffer
ENV PYTHONUNBUFFERED 1

# Updating the os
# RUN apk update 

# Copying requirement file
COPY requirements.txt /code/

# Upgrading pip version
RUN pip install --upgrade pip

# Installing dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /code/
RUN sed -i 's/\r$//g' /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

# Copying all the files in our project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]