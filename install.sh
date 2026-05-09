#!/bin/bash

# APK Installer - Bootstrap Script
# This script installs 'uv' if missing and then installs the 'apk-installer' tool.

set -e

echo "🚀 Installing APK Installer..."

# 1. Check for uv
if ! command -v uv &> /dev/null; then
    echo "📦 'uv' not found. Installing uv (modern python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 2. Install the tool
# Note: In a real scenario, this would point to the PyPI package or GitHub URL
# For now, we'll assume we are installing from the current directory for testing
# but we can also point it to a git repo:
# uv tool install git+https://github.com/username/apk-installer.git

echo "🛠️ Installing apk-installer tool..."
uv tool install . --force

echo ""
echo "✅ Done! You can now run the tool by typing: apk-installer"
echo "⚠️  Make sure 'adb' is installed and in your PATH."
