FROM python:3

ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

RUN apt-get -y update
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y sudo
RUN apt-get install -y vim
RUN apt-get install net-tools

WORKDIR /srv/docker-server

COPY requirements.txt requirements.txt
# COPY . . # volumes

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt-get install -y cron