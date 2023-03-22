FROM python:3.8-slim-buster

ARG BRANCH=feature/concordance

RUN apt-get clean \
    && apt-get update -qq \
    && apt-get install -y git \
    && mkdir /usr/bin/app \
    && cd /usr/bin/app \
    && git clone https://github.com/mskcc/collect-qc.git --branch ${BRANCH} \
    && pip install -r collect-qc/requirements.txt

# Mount the repo onto a volume
VOLUME /usr/bin/app/collect-qc

# Change to the directory with the config.yaml and data files
WORKDIR /usr/bin/app

CMD [ "python", "/usr/bin/app/collect-qc/scripts/main.py" ]