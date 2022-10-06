FROM python:3.10-slim-buster

LABEL org.opencontainers.image.description "Python docker image to be used by ValiFN"
LABEL maintainer="Valispace DevOps <devops@valispace.com>"

# Activate unattended package installation with default answers for all questions
ENV DEBIAN_FRONTEND="noninteractive"
# Suppress apt-key warning about standard out not being a terminal (use in this script is safe)
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE="DontWarn"
# Suppress pip warning about running as root user (use in this script is safe)
ENV PIP_ROOT_USER_ACTION="ignore"
# Make sure all python messages always reach the console
ENV PYTHONUNBUFFERED=1

# Copy application source code to docker image
COPY ./ /opt/valispace/valifn

# Use bash as shell
SHELL [ "/bin/bash", "-c" ]

# Stop execution immediately when a command fails
RUN set -e

# Cleanup caches and unnecessary files
RUN \
    apt-get --quiet --assume-yes autoremove && \
    apt-get --quiet autoclean && \
    rm --force --recursive /var/cache/apt/* && \
    rm --force --recursive /var/lib/apt/lists/*
# Create logs folders
RUN \
    mkdir --parents /var/log/valispace/valifn

# Create 'valispace' user (non-root)
RUN \
    useradd --create-home --home-dir /home/valispace --shell /bin/bash --password "$( openssl passwd -1 valispace )" valispace

# Set the application owner
RUN \
    chown --quiet --recursive valispace:valispace /opt/valispace/valifn && \
    chown --quiet --recursive valispace:valispace /var/log/valispace/valifn

# Set the default user
USER valispace

# Set working directory
WORKDIR /home/valispace

# Create a python virtual environment
RUN \
    python -m venv .venv

# Install python dependencies for the application
RUN \
    source .venv/bin/activate && \
    pip --require-virtualenv --no-input --exists-action w install --upgrade pip wheel && \
    pip --require-virtualenv --no-input --exists-action w install --requirement /opt/valispace/valifn/requirements.txt

# No need to track logs because container is constantly
# destroyed after each execution or failure
CMD ["tail", "--follow", "/dev/null"]
