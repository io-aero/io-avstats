FROM python:3.10.9 as base

LABEL maintainer="IO Aero"

ARG APP
ARG SERVER_ADDRESS
ARG SERVER_PORT
ENV APP=${APP}
ENV SERVER_PORT=${SERVER_PORT}
SHELL ["/bin/bash", "-c"]

EXPOSE ${SERVER_PORT}

WORKDIR /home

COPY .settings.io_avstats.toml ./
COPY .streamlit/config.toml ./.streamlit/
COPY .streamlit/secrets_4_dockerfile.toml ./.streamlit/secrets.toml
COPY Makefile ./
COPY Pipfile ./
COPY settings.io_avstats_4_dockerfile.toml ./settings.io_avstats.toml
COPY src/streamlit_apps/${APP}.py ./${APP}.py

RUN make pipenv-prod

ENTRYPOINT ["pipenv", "run", "streamlit", "run", "${APP}.py", "--server.port=${SERVER_PORT}"]
