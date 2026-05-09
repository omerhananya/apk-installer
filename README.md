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

### Quick Install
Run the following command to install the tool via `uv`. This will handle the environment and add `apk-installer` to your PATH:

```bash
curl -sSL https://raw.githubusercontent.com/omerhananya/apk-installer/main/install.sh | sh
```

*Note: If this is a private repository, you will need to provide a GitHub Personal Access Token in the request.*

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
