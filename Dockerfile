FROM ubuntu:18.04
# changes from shell to bash, which is useful in running some commands
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt update
RUN apt-get install -y unzip python3.8 python3-pip
RUN python3.8 -m pip install --upgrade pip

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT python3.8 flask_api.py
