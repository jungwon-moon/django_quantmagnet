FROM python:3

ENV PYTHONDONTWRITEBYECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update

WORKDIR /srv/docker-server

COPY requirements.txt requirements.txt
# COPY . . # volumes

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]