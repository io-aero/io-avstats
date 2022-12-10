FROM python:3.10.9 as base

LABEL maintainer="IO Aero"

ARG APP
ENV APP=${APP}
SHELL ["/bin/bash", "-c"]
WORKDIR /home

COPY .streamlit/config.toml ./.streamlit/
COPY .streamlit/secrets.toml ./.streamlit/
COPY Makefile ./
COPY Pipfile ./
COPY settings.io_avstats.toml ./
COPY src/${APP}_app/${APP}.py ./${APP}.py

EXPOSE 8501

RUN make pipenv-prod

ENTRYPOINT ["pipenv", "run", "streamlit", "run", "${APP}.py", "--server.port=8501", "--server.address=0.0.0.0"]
