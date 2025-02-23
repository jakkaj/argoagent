#!/bin/bash
# Exit immediately if a command exits with a non-zero status
set -e

# Check if the .env file exists in the current directory
if [[ ! -f .env ]]; then
  echo "Error: .env file not found in the current directory."
  exit 1
fi

# Load variables from the .env file
export $(grep -v '^#' .env | xargs)

# Verify the OPENAI_API_KEY variable is set
if [[ -z "${OPENAI_API_KEY}" ]]; then
  echo "Error: OPENAI_API_KEY is not set in the .env file."
  exit 1
fi

# Create the Kubernetes secret using the OPENAI_API_KEY from the .env file
kubectl create secret generic openai-api-key \
  --from-literal=OPENAI_API_KEY="${OPENAI_API_KEY}" \
  --namespace argo

echo "Kubernetes secret 'openai-api-key' created successfully."
