FROM python:3.12

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

## Generate Public/Private Key Pair
# RUN apt-get update && apt-get install -y openssh-client \
#     && mkdir -p /keys && chmod 700 /keys \
#     && ssh-keygen -t rsa -b 4096 -f /keys/id_rsa -N "" \
#     && chmod 600 /keys/id_rsa \
#     && chmod 644 /keys/id_rsa.pub

# Set the working directory in the container and copy python files
WORKDIR /app
COPY trippy-mako/core /app

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Set an environment variable for the config directory
ENV CONFIG_DIR=/config

# Ensure the config directory exists (will be replaced if mounted)
RUN mkdir -p /config

# Run Trippy on container startup
ENTRYPOINT ["bash", "-c", "python3 trippyMako.py; exec bash"]