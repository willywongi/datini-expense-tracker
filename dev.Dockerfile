# This dockerfile should be used during development of this project.
# Write a docker-compose.override.yaml to use this.
FROM python:3.9-buster
ARG DJANGO_PORT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install -U pipenv
WORKDIR /app

# Adding Pipfiles
COPY Pipfile Pipfile

# Lock & install dependencies:
# --deploy: Abort if the Pipfile.lock is out-of-date, or Python version is wrong.
# --system: System pip management (don't make an isolated env, since we're in a container)
# --dev: Install both develop and default packages
RUN set -ex && pipenv lock && pipenv install --deploy --system --dev

# Application files will be mounted in /app/datini
# Check docker-compose.override.yaml for configuration.
WORKDIR /app/datini

# Tell Docker what port we're exposing 
EXPOSE $DJANGO_PORT

# This is the base command; runserver will be managed by the
# docker-compose file.
ENTRYPOINT ["python", "manage.py"]
