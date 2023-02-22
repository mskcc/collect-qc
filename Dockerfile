FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app
COPY requirements.txt requirements.txt
COPY main.py main.py
COPY metric.py metric.py

RUN pip install -r requirements.txt

CMD ["python", "./collect-qc/main.py"]