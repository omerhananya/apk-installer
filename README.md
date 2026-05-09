# APK Installer

A cross-platform CLI tool to install multiple APK files to multiple Android devices simultaneously via a matrix-style TUI.

## Features
- **Hybrid Input:** Pass APKs as arguments or select them in the TUI.
- **Matrix Selection:** Toggle which phone gets which app.
- **Parallel Install:** Installs APKs to all devices at once for maximum speed.
- **Cross-Platform:** Works on Windows, Mac, and Linux.

## Prerequisites
- [Android Platform Tools (ADB)](https://developer.android.com/tools/releases/platform-tools) must be installed and in your PATH.
- Python 3.10+

## Installation

### Using uv (Recommended)
```bash
uv tool install .
```

### Using pip
```bash
pip install .
```

## Usage
Run without arguments to pick APKs in the current directory:
```bash
apk-installer
```

Or pass specific APK files:
```bash
apk-installer app1.apk app2.apk
```

## License
MIT
