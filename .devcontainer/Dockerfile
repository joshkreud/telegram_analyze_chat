# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.154.0/containers/python-3/.devcontainer/base.Dockerfile

ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends  unixodbc-dev \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

COPY .devcontainer/requirements.txt /tmp/pip-tmp-dev/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp-dev/requirements.txt \
    && rm -rf /tmp/pip-tmp-dev