# APK Installer Design Specification
**Date:** 2026-05-09
**Status:** Approved

## 1. Purpose
A cross-platform CLI tool to install multiple APK files to multiple Android devices simultaneously via a matrix-style TUI.

## 2. Core Requirements
- **Hybrid Input:** Support command-line arguments for APK paths or an interactive TUI file picker if none are provided.
- **Device Discovery:** Use ADB to list all connected Android devices (serial, model name).
- **Selection Matrix:** A reactive TUI where users toggle installs for specific APK/Device combinations.
- **Parallel Installation:** Execute `adb install` commands in parallel across multiple devices.
- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **Prerequisite Check:** Verify `adb` binary is available in PATH before starting.

## 3. Tech Stack
- **Language:** Python 3.10+
- **TUI Framework:** [Textual](https://textual.textualize.io/) (CSS-based, reactive)
- **ADB Interaction:** Subprocess calls to the system `adb` binary.
- **Concurrency:** `asyncio` for managing simultaneous install processes.

## 4. Components

### 4.1 CLI Entry Point
- Parse `sys.argv` for `.apk` files.
- If empty, launch `FilePickerApp`.
- Once APKs are confirmed, launch `MatrixApp`.

### 4.2 Device Manager
- Function `get_devices()`: Runs `adb devices -l`.
- Returns list of `Device` objects (serial, model, status).

### 4.3 Matrix TUI (The Core)
- **Header:** Shows device count and general help.
- **Grid:** 
    - Rows: APK files.
    - Columns: Devices.
    - Cells: Checkbox/Toggle indicating "Install this APK on this Device".
- **Footer:** "Install" button and status bar.

### 4.4 Installer Engine
- Function `install_parallel(mapping)`: Takes a dictionary of `{device_serial: [list_of_apks]}`.
- Uses `asyncio.create_subprocess_exec` to run `adb -s <serial> install <path>`.
- Reports real-time progress/success/failure back to the TUI.

## 5. User Workflow
1. User runs `apk-installer`.
2. Tool checks for `adb`. If missing, prints error and exits.
3. If no files passed, user selects APKs in a TUI picker.
4. Matrix TUI appears with devices as columns and APKs as rows.
5. User toggles cells, then hits "Install".
6. TUI shows progress bars for each installation.
7. Final report shows success/failure for each combination.

## 6. Constraints & Safety
- **No ADB:** Show clear instructions to install Android Platform Tools.
- **Locked Devices:** Detect if a device is "unauthorized" or "offline" and flag in TUI.
## 7. Distribution Strategy
- **Format:** Standard Python package with `pyproject.toml`.
- **Primary Tool:** [uv](https://astral.sh/uv) for management and execution.
- **Installation Options:**
    - `uv tool install .` (from source)
    - `pip install .` (from source)
    - Potential `curl | sh` installer script that bootstraps `uv` and installs the package.
- **Dependency Management:** All dependencies (textual, etc.) strictly versioned in `pyproject.toml`.
