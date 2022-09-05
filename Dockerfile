# Alpine is a lightweight Linux distribution that is suited for Docker containers.
FROM python:3.9-alpine3.16
LABEL maintainer="Tejas Kale"

# The line below ensures that any output from Python is immediately dumped to console.
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements-dev.txt /tmp/requirements-dev.txt
COPY ./app /app
WORKDIR /app

# The port on our Docker container through which we can communicate with it via our local machine.
EXPOSE 8000

# Set default argument values.
ARG DEV=false

# Docker creates an image layer for every command. If we want to run multiple commands and
# keep our image lightweight, we can concatenate them using `&& \`.
# A Dockerfile is executed as the root user inside a Linux environment and a container also
# runs with the root user by default. In order to product our container/application in case it
# is compromised, it is recommended to create a new user (here `django-user`) which has limited
# but necessary privileges. Hence, we create a user without any password and no home directory.
# The latter choice is intended to keep the image light.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements-dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

# When a container is started from this image, it will be accessible as a django-user and not root.
USER django-user
