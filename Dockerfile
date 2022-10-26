FROM python:3.11.0-slim

LABEL maintainer="Valispace DevOps <devops@valispace.com>"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE="settings.docker"

ARG DEBIAN_FRONTEND=noninteractive \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

# Copy the application source code to docker image and install dependencies
COPY ./ /valifn
WORKDIR /valifn

RUN set -e && \
    # Install python dependencies for the application
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement requirements.txt

# No need to track logs because container is constantly
# destroyed after each execution or failure
CMD ["tail", "-f", "/dev/null"]
