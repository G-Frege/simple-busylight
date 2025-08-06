#!/bin/bash

set -e

VERSION=$(cat version)

echo "Building client..."
pyinstaller --name simple-busylight --onefile simple_busylight/client.py

echo "Building server..."
pyinstaller --name simple-busylight-server --onefile simple_busylight/server.py

mkdir -p build/dist
cp dist/simple-busylight build/dist/
cp dist/simple-busylight-server build/dist/
