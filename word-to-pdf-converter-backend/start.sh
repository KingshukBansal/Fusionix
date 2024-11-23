#!/bin/bash

echo "Applying Kubernetes manifests for all services..."

# List of service directories containing manifest folders
services=("gateway" "metadata" "download" "docx-to-pdf-converter" "notification" "rabbit")

# Loop through each service and apply its manifest files
for service in "${services[@]}"; do
    echo "Applying manifests for $service..."
    kubectl apply -f ./$service/manifest
done

echo "All Kubernetes manifests applied successfully. Verify with kubectl get pods and kubectl get services."
