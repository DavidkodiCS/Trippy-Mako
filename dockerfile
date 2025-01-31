FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y coturn

# Set up Coturn configuration
RUN echo "listening-port=5349\nfingerprint\nno-auth\nno-tls\nno-dtls\nno-tcp-relay" | tee /etc/turnserver.conf > /dev/null

# Set the working directory in the container
WORKDIR /work

# Copy your Python files into the container's /work directory
COPY Trippy-Mako/trippy-mako/core /work

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Expose the Coturn listening port
EXPOSE 5349/udp
EXPOSE 5349/tcp

# Run Coturn on container startup
ENTRYPOINT ["sh", "-c", "turnserver -c /etc/turnserver.conf -v & exec bash"]
