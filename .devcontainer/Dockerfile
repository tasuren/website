FROM mcr.microsoft.com/devcontainers/base:debian

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    git \
    nano \
    vim-tiny \
    curl \
    && apt-get auto-remove -y \
    && apt-get clean -y

RUN curl -fsSL https://bun.sh/install | bash
