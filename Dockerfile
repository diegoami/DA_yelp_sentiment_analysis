FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install -e .
RUN mkdir data



