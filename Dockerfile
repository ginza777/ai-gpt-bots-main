# pull official base image
FROM python:3.11-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install system dependencies
RUN apt-get update && apt-get install -y gettext

COPY ./requirements.txt requirements.txt


# install dependencies
RUN pip install -r requirements.txt

# copy project
COPY . .

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/locale
WORKDIR $APP_HOME

# copy project
COPY . $APP_HOME

RUN ["chmod", "+x", "/home/app/web/entrypoint.sh"]
