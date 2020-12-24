FROM python:3.9-buster

RUN \
    apt-get update \
    && apt-get install --no-install-recommends -y unixodbc-dev\
    && rm -rf /var/lib/{apt,dpkg,cache,log}

WORKDIR /tmp
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN useradd -ms /bin/bash developer && chown -R developer /home/developer
USER developer

ENV SHELL /bin/bash