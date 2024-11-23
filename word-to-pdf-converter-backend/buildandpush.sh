#!/bin/bash

# Set Docker Hub username
DOCKER_USERNAME="kingshukbansal"

# List of services
services=("gateway" "metadata" "download" "docx-to-pdf-converter" "notification")

# Loop through each service
for service in "${services[@]}"; do
    echo "Building Docker image for $service..."
    docker build -t $DOCKER_USERNAME/rapidfort-$service:latest ./$service
    echo "Pushing Docker image for $service to Docker Hub..."
    docker push $DOCKER_USERNAME/rapidfort-$service:latest
done

echo "All Docker images built and pushed successfully!"
