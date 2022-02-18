FROM python:3

ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get install -y sudo
RUN apt-get install -y vim

WORKDIR /srv/docker-server

COPY requirements.txt requirements.txt
# COPY . . # volumes

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get install -y cron