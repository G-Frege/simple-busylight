#!/bin/bash

set -e

VERSION=$(cat version)
PKG_NAME=simple-busylight
BUILD_DIR=build/deb/${PKG_NAME}_${VERSION}

# Clean up
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/local/bin"
mkdir -p "$BUILD_DIR/lib/systemd/system"

# Copy files
cp debian/control "$BUILD_DIR/DEBIAN/"
cp debian/postinst "$BUILD_DIR/DEBIAN/"
cp debian/simple-busylightd.service "$BUILD_DIR/lib/systemd/system/"
cp build/dist/simple-busylight "$BUILD_DIR/usr/local/bin/"
cp build/dist/simple-busylightd "$BUILD_DIR/usr/local/bin/"
chmod +x "$BUILD_DIR/usr/local/bin/"*

# Build package
dpkg-deb --build "$BUILD_DIR"
mv "$BUILD_DIR.deb" build/
