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

# Create application log
RUN mkdir --parents /var/log/valispace/valifn

# Install application dependencies (apt-get)
# Install application dependencies (pip)
RUN pip --no-input --exists-action w install --upgrade pip wheel setuptools
RUN pip --no-input --exists-action w install --requirement /opt/valispace/valifn/requirements.txt

# Cleanup caches (apt-get)
RUN apt-get --quiet --assume-yes autoremove && apt-get --quiet autoclean && rm --force --recursive /var/lib/apt/lists/* && rm --force --recursive /var/cache/apt/*
# Cleanup caches (pip)
RUN pip cache purge

# No need to track logs because container is constantly
# destroyed after each execution or failure
CMD ["tail", "--follow", "/dev/null"]
