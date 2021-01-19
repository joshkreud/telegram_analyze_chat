ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends  unixodbc-dev \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

USER vscode
WORKDIR /home/vscode

COPY --chown=vscode:vscode requirements.txt ./pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r ./pip-tmp/requirements.txt \
    && rm -rf ./pip-tmp

COPY --chown=vscode:vscode .devcontainer/requirements.txt ./pip-tmp-dev/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r ./pip-tmp-dev/requirements.txt \
    && rm -rf ./pip-tmp-dev

RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyterlab-plotly plotlywidget

RUN python3 -m spacy download nl_core_news_sm \
    && python3 -m spacy download en_core_web_sm \
    && python3 -m spacy download de_core_news_sm \
    && python3 -m spacy download xx_ent_wiki_sm

ENV PATH="/home/vscode/.local/bin:${PATH}"