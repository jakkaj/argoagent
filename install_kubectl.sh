#!/bin/bash

# Check if kubectl is already installed
if command -v kubectl > /dev/null 2>&1; then
    echo "kubectl is already installed"
    exit 0
fi

# Download kubectl binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Verify download success
if [ $? -ne 0 ]; then
    echo "Failed to download kubectl"
    exit 1
fi

chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl

echo "kubectl installation completed."
