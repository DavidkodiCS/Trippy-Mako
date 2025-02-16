FROM python:3.12

# Install and set up Coturn configuration
RUN apt-get update && apt-get install -y coturn
RUN echo "listening-port=5349\nfingerprint\nno-auth\nno-tls\nno-dtls\nno-tcp-relay" | tee /etc/turnserver.conf > /dev/null

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

# Run Coturn on container startup
ENTRYPOINT ["sh", "-c", "turnserver -c /etc/turnserver.conf -v & exec bash"]
