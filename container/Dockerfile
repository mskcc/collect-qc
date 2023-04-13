FROM python:3.8-slim-buster

ARG BRANCH=main

RUN apt-get clean \
    && apt-get update -qq \
    && apt-get install -y git \
    && mkdir /usr/bin/collectqc \
    && cd /usr/bin/collectqc \
    && git clone https://github.com/mskcc/collect-qc.git --branch ${BRANCH} \
    && pip install -r collect-qc/requirements.txt

# Mount the repo onto a volume
VOLUME /usr/bin/collectqc/collect-qc

# Change to the directory with the config.yaml and data files
WORKDIR /usr/bin/collectqc

CMD [ "python", "/usr/bin/collectqc/collect-qc/scripts/main.py" ]