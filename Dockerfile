# Use the official Miniconda3 base image
FROM continuumio/miniconda3

# Install locales and generate en_US.UTF-8
RUN apt-get update && \
    apt-get install -y locales && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV REPO_MODULE=ioavstats \
    REPO_UNDERS=io_avstats \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    ENV_FOR_DYNACONF=prod

# Set the working directory inside the container
WORKDIR /app

# Argument for PYPI_PAT
ARG PYPI_PAT
ENV PYPI_PAT=${PYPI_PAT}

# Copy the environment.yml file to the container
COPY config/environment_streamlit.yml ./environment.yml

# Create the conda environment
RUN conda env create -f environment.yml && conda clean -a

# Activate the environment
SHELL ["conda", "run", "-n", "ioavstats", "/bin/bash", "-c"]

# Copy the application code to the container
COPY .streamlit ./.streamlit/
COPY ${REPO_MODULE}/ ./${REPO_MODULE}/
COPY resources/Images ./resources/Images/
COPY .settings.io_aero.toml .
COPY logging_cfg.yaml .
COPY settings.io_aero.toml .

# Expose the port for Streamlit
EXPOSE 8501

# Healthcheck to monitor the app status
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Set the entrypoint for Streamlit
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ioavstats", "streamlit", "run", "ioavstats/Menu.py", "--server.port=8501", "--server.address=0.0.0.0"]
