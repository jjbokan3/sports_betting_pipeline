# Use the official Python base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /dagster_project

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Set Dagster home inside the .docker folder
ENV DAGSTER_HOME=/dagster_project/.docker/dagster_home
RUN mkdir -p $DAGSTER_HOME

# Expose Dagit port
EXPOSE 3000

# Set entrypoint script
ENTRYPOINT ["./.docker/scripts/run.sh"]