# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV REPO_MODULE=ioavstats
ENV REPO_UNDERS=io_avstats

# Set the working directory inside the container
WORKDIR /app

# Argument for PYPI_PAT
ARG PYPI_PAT
ENV PYPI_PAT=${PYPI_PAT}

# Install necessary packages for Miniconda, locales, and git
RUN apt-get update && \
    apt-get install -y bash wget ca-certificates libstdc++6 build-essential locales git curl && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Set environment variables for locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Determine architecture and download appropriate Miniconda installer
RUN echo "**** install Miniconda ****" && \
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh; \
    elif [ "$ARCH" = "aarch64" ]; then \
        wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /tmp/miniconda.sh; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean -a -y && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> /etc/bash.bashrc && \
    echo "conda activate base" >> /etc/bash.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Copy the environment file to the container
COPY config/environment.yml .

# Replace placeholder with actual value and debug output
RUN echo "PYPI_PAT: $PYPI_PAT" && \
    sed -i "s|\${PYPI_PAT}|${PYPI_PAT}|g" environment.yml && \
    cat environment.yml

# Install dependencies from the environment file
RUN /opt/conda/bin/conda env create -f environment.yml

# Copy the application code to the container
COPY ${REPO_MODULE}/ ./${REPO_MODULE}/
COPY scripts/ ./scripts/
COPY .settings.io_aero.toml .
COPY logging_cfg.yaml .
COPY pyproject.toml .
COPY run_${REPO_UNDERS}.sh .
COPY settings.io_aero.toml .

# Set environment variables for the application
ENV ENV_FOR_DYNACONF=prod
ENV PYTHONPATH=./${REPO_MODULE}:./scripts

# Make the scripts executable
RUN chmod +x entrypoint.sh
RUN chmod +x run_${REPO_UNDERS}.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Ensure the environment is activated and run the application
CMD ["bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate ${REPO_MODULE} && ./run_${REPO_UNDERS}.sh"]
