FROM python:3.12

# Install system dependencies
RUN apt-get update && apt-get install -y coturn

# Set the working directory in the container
WORKDIR /work

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt