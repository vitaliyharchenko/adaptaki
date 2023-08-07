# Fetching official base image for python
FROM python:3

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
RUN pip install gunicorn

# Installing dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Copying all the files in our project
COPY . /code/