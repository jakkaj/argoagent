#!/bin/bash

# filepath: build_image.sh
# Usage: ./build_image.sh <image_name>

image_name=$1

if [ -z "$image_name" ]; then
  echo "Error: Image name must be provided as an argument."
  exit 1
fi

docker build -f ./"$image_name"/Dockerfile -t k3d-registry.localhost:5000/"$image_name":latest ./"$image_name"
docker push k3d-registry.localhost:5000/"$image_name":latest
k3d image import k3d-registry.localhost:5000/"$image_name":latest -c argoagent-cluster