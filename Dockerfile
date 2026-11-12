# Use the official, minimal Python 3.12 Debian image
FROM python:3.12-slim

# Install the restic binary via the Linux package manager
RUN apt-get update && \
    apt-get install -y restic && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary configuration and source code
COPY pyproject.toml ./
COPY src/ ./src/

# Install the backup-verifier CLI tool into the container
RUN pip install --no-cache-dir .

# Define the default command when the container boots
ENTRYPOINT ["backup-verifier"]
