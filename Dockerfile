FROM python:3.7

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN python -c "import nltk; nltk.download('punkt')"



