FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nano
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install -e .



