FROM python:latest

COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY . /opt/app

WORKDIR "/opt/app"
