FROM python:3.8-slim-buster

ARG FEATURE_BRANCH=feature/hsmetrics

WORKDIR /usr/bin

# Copy data from the volume into the container
COPY . .

RUN apt-get clean \
    && apt-get update -qq \
    && apt-get install -y git \
    && cd /usr/bin \
    && git clone https://github.com/mskcc/collect-qc.git --branch ${FEATURE_BRANCH} \
    && pip install -r collect-qc/requirements.txt 

CMD ["python", "collect-qc/main.py"]