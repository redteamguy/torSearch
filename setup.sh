#!/bin/bash

# Installing Python packages using pip
echo "[+] Installing Required packages..."
pip install requests beautifulsoup4

echo "[+] Installing Tor..."
sudo apt install -y tor

echo "Starting and enabling tor"
sudo systemctl start tor
sudo systemctl enable tor

echo "[+] Almost there!"
mkdir results 
# Check if installations were successful
if [[ $? -eq 0 ]]; then
    echo "\n\n[+] Setup complete. Please run the python file to continue."
else
    echo "[!] An error occurred during installation."
    exit 1
fi
