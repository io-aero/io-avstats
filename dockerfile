FROM python:3.10.10 as base

LABEL maintainer="IO-Aero"

ARG APP
ARG MODE
ARG SERVER_ADDRESS
ARG SERVER_PORT

ENV APP=${APP}
ENV MODE=${MODE}
ENV SERVER_PORT=${SERVER_PORT}
ENV SQLALCHEMY_SILENCE_UBER_WARNING=1

SHELL ["/bin/bash", "-c"]

EXPOSE ${SERVER_PORT}

WORKDIR /home

COPY .settings.io_avstats_4_dockerfile.toml ./.settings.io_avstats.toml
COPY .streamlit/config.toml.${APP} ./.streamlit/config.toml
COPY .streamlit/secrets_4_dockerfile.toml ./.streamlit/secrets.toml
COPY Makefile ./
COPY Pipfile.${APP} ./Pipfile
COPY settings.io_avstats_4_dockerfile.toml ./settings.io_avstats.toml
COPY src/ioavstats/${APP}.py ./${APP}.py
COPY src/ioavstats/utils.py ./utils.py

RUN make pipenv-prod

ENTRYPOINT pipenv run streamlit run ${APP}.py --server.port=${SERVER_PORT} -- --host Cloud --mode ${MODE}
