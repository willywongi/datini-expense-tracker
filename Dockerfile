# Install and run the backend server
FROM python:3.9-buster
ARG DJANGO_PORT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install -U pipenv
WORKDIR /app

# Adding Pipfile with pinned dependencies
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

# Install dependencies:
# --deploy: Abort if the Pipfile.lock is out-of-date, or Python version is wrong.
# --system: System pip management (don't make an isolated env, since we're in a container)
RUN set -ex && pipenv install --deploy --system

COPY datini datini/
WORKDIR /app/datini

# Set permission for entrypoint script
RUN ["chmod", "a+x", "run.sh"]

# Tell Docker what port we're exposing 
EXPOSE $DJANGO_PORT

ENTRYPOINT ["/app/datini/run.sh"]
