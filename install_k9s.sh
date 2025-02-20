#!/bin/bash

# Define the version and architecture
K9S_VERSION="v0.27.4"
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
fi

# Check if k9s is already installed
if command -v k9s > /dev/null 2>&1; then
    echo "k9s is already installed"
    exit 0
fi

# Download k9s tarball with corrected URL pattern
curl -Lo k9s.tar.gz "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_${ARCH}.tar.gz"

# Verify download success
if [ $? -ne 0 ]; then
    echo "Failed to download k9s"
    exit 1
fi

# Extract, install and cleanup
tar -xzf k9s.tar.gz
if [ $? -ne 0 ]; then
    echo "Failed to extract k9s tarball"
    exit 1
fi

chmod +x k9s
sudo mv k9s /usr/local/bin/k9s
rm k9s.tar.gz

echo "k9s installation completed."
