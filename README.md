# APK Installer

A cross-platform CLI tool to install multiple APK files to multiple Android devices simultaneously via a matrix-style TUI.

## Features
- **Hybrid Input:** Pass APKs as arguments or select them in the TUI.
- **Matrix Selection:** Toggle which phone gets which app.
- **Parallel Install:** Installs APKs to all devices at once for maximum speed.
- **Cross-Platform:** Works on Windows, Mac, and Linux.
- **Zero-Dependency Binary:** Optional standalone executable (no Python required).

## Prerequisites
- [Android Platform Tools (ADB)](https://developer.android.com/tools/releases/platform-tools) must be installed and in your PATH.
- Python 3.10+ (only if not using the standalone binary).

## Installation

### Option 1: Quick Install (Recommended)
Install instantly via `uv`:
```bash
curl -sSL https://raw.githubusercontent.com/user/repo/main/install.sh | sh
```

### Option 2: Standalone Binary
Download the pre-built `apk-installer` binary for your OS from the [Releases](https://github.com/user/repo/releases) page. No Python installation is required.

### Option 3: Using uv/pip
```bash
uv tool install .
# OR
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

### Controls
- **Arrows**: Navigate the matrix.
- **Space/Enter**: Toggle selection for a device/APK.
- **'i'**: Start parallel installation.
- **'q'**: Quit.

## Development
To build the standalone executable yourself:
```bash
uv run python build_exe.py
```
The binary will be generated in the `dist/` folder.

## License
MIT
