#!/bin/bash

# Check if kind is already installed
if command -v kind > /dev/null 2>&1; then
    echo "kind is already installed"
    exit 0
fi

# Download kind binary
curl -Lo kind https://kind.sigs.k8s.io/dl/v0.17.0/kind-linux-amd64

# Verify download success
if [ $? -ne 0 ]; then
    echo "Failed to download kind"
    exit 1
fi

chmod +x kind
sudo mv kind /usr/local/bin/kind

echo "kind installation completed."
