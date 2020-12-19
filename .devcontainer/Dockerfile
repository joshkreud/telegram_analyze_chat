FROM python:3.9-buster

RUN \
    apt-get update \
    && apt-get install --no-install-recommends -y unixodbc-dev\
    && rm -rf /var/lib/{apt,dpkg,cache,log}

RUN useradd -ms /bin/bash developer
USER developer
WORKDIR /home/developer

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV SHELL /bin/bash