FROM python:3.12

# Install Crypto
RUN pip install pycryptodome 

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

# Expose the Coturn listening port
EXPOSE 5349/udp
EXPOSE 5349/tcp

# Run Trippy on container startup
ENTRYPOINT ["bash", "-c", "python3 trippyMako.py; exec bash"]
