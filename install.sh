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
echo "🛠️ Installing apk-installer tool..."
# Prefer installing from the remote repo so the tool is correctly linked to source
uv tool install git+https://github.com/omerhananya/apk-installer.git --force

echo ""
echo "✅ Done! You can now run the tool by typing: apk-installer"
echo "⚠️  Make sure 'adb' is installed and in your PATH."
