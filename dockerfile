FROM python:3.10.9 as base

LABEL maintainer="IO Aero"

ARG APP
ARG SERVER_ADDRESS
ARG SERVER_PORT
ENV APP=${APP}
ENV SERVER_ADDRESS=${SERVER_ADDRESS}
ENV SERVER_PORT=${SERVER_PORT}
SHELL ["/bin/bash", "-c"]

EXPOSE ${SERVER_PORT}

WORKDIR /home

COPY .settings.io_avstats.toml ./
COPY .streamlit/config.toml ./.streamlit/
COPY .streamlit/secrets.toml ./.streamlit/
COPY Makefile ./
COPY Pipfile ./
COPY settings.io_avstats.toml ./
COPY src/${APP}_app/${APP}.py ./${APP}.py

RUN make pipenv-prod

ENTRYPOINT ["pipenv", "run", "streamlit", "run", "${APP}.py", "--server.port=${SERVER_PORT}", "--server.address=${SERVER_ADDRESS}"]
