# APK Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a cross-platform CLI tool for parallel APK installation across multiple Android devices using a Textual TUI.

**Architecture:** Hybrid CLI/TUI entry point. Textual matrix for selection. Asyncio subprocesses for parallel ADB installs.

**Tech Stack:** Python 3.10+, Textual, asyncio, uv.

---

### Task 1: Project Initialization & Prerequisite Check

**Files:**
- Create: `pyproject.toml`
- Create: `src/apk_installer/cli.py`
- Create: `src/apk_installer/adb.py`
- Test: `tests/test_adb.py`

- [ ] **Step 1: Create `pyproject.toml` with dependencies**
```toml
[project]
name = "apk-installer"
version = "0.1.0"
description = "Parallel APK installer for multiple Android devices"
dependencies = [
    "textual>=0.50.0",
]

[project.scripts]
apk-installer = "apk_installer.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 2: Implement ADB availability check**
```python
# src/apk_installer/adb.py
import subprocess
import shutil

def check_adb_exists() -> bool:
    return shutil.which("adb") is not None

def get_adb_version() -> str:
    try:
        return subprocess.check_output(["adb", "--version"], text=True).splitlines()[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
```

- [ ] **Step 3: Write test for ADB check**
```python
# tests/test_adb.py
from apk_installer.adb import check_adb_exists

def test_check_adb_exists():
    # This assumes adb is installed on the dev machine
    assert check_adb_exists() is True
```

- [ ] **Step 4: Create entry point with ADB check**
```python
# src/apk_installer/cli.py
import sys
from apk_installer.adb import check_adb_exists

def main():
    if not check_adb_exists():
        print("Error: 'adb' not found in PATH.")
        print("Please install Android Platform Tools: https://developer.android.com/tools/releases/platform-tools")
        sys.exit(1)
    print("ADB found. Ready.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Verify and commit**
Run: `uv run apk-installer`
Expected: "ADB found. Ready." (or error if missing)
```bash
git add pyproject.toml src/ tests/
git commit -m "chore: project init and adb check"
```

---

### Task 2: Device Discovery

**Files:**
- Modify: `src/apk_installer/adb.py`
- Test: `tests/test_adb.py`

- [ ] **Step 1: Implement device listing**
```python
# src/apk_installer/adb.py (add)
from dataclasses import dataclass

@dataclass
class Device:
    serial: str
    model: str
    status: str

def get_devices() -> list[Device]:
    output = subprocess.check_output(["adb", "devices", "-l"], text=True)
    devices = []
    for line in output.splitlines()[1:]:
        if not line.strip(): continue
        parts = line.split()
        serial = parts[0]
        status = parts[1]
        model = "Unknown"
        for p in parts:
            if p.startswith("model:"):
                model = p.split(":")[1]
        devices.append(Device(serial, model, status))
    return devices
```

- [ ] **Step 2: Add test for device parsing**
```python
# tests/test_adb.py (add)
from apk_installer.adb import get_devices

def test_get_devices():
    devices = get_devices()
    assert isinstance(devices, list)
    if devices:
        assert hasattr(devices[0], 'serial')
```

- [ ] **Step 3: Commit**
```bash
git commit -am "feat: device discovery logic"
```

---

### Task 3: The Selection Matrix TUI

**Files:**
- Create: `src/apk_installer/tui.py`
- Modify: `src/apk_installer/cli.py`

- [ ] **Step 1: Implement basic Matrix App using Textual**
```python
# src/apk_installer/tui.py
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Label

class MatrixApp(App):
    CSS = """
    DataTable {
        height: 1fr;
        border: solid green;
    }
    """
    def __init__(self, apks: list[str], devices: list):
        super().__init__()
        self.apks = apks
        self.devices = devices

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Select APKs to install on {len(self.devices)} devices")
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("APK", width=30)
        for dev in self.devices:
            table.add_column(f"{dev.model}\n({dev.serial})")
        
        for apk in self.apks:
            table.add_row(apk, *["[ ]" for _ in self.devices])
```

- [ ] **Step 2: Update CLI to launch TUI**
```python
# src/apk_installer/cli.py
from apk_installer.adb import check_adb_exists, get_devices
from apk_installer.tui import MatrixApp

def main():
    if not check_adb_exists():
        # ... error logic ...
        sys.exit(1)
    
    apks = [arg for arg in sys.argv[1:] if arg.endswith(".apk")]
    devices = get_devices()
    
    if not apks:
        print("No APKs provided. (TUI file picker coming in Task 5)")
        return

    app = MatrixApp(apks, devices)
    app.run()
```

- [ ] **Step 3: Commit**
```bash
git commit -am "feat: basic matrix tui"
```

---

### Task 4: Interactive Matrix & Parallel Installation

**Files:**
- Modify: `src/apk_installer/tui.py`
- Modify: `src/apk_installer/adb.py`

- [ ] **Step 1: Implement Cell Toggle logic**
```python
# src/apk_installer/tui.py
# Add on_data_table_cell_selected handler to toggle "[ ]" to "[x]"
```

- [ ] **Step 2: Implement Async Installer Engine**
```python
# src/apk_installer/adb.py
import asyncio

async def install_apk(serial: str, apk_path: str):
    proc = await asyncio.create_subprocess_exec(
        "adb", "-s", serial, "install", apk_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return proc.returncode == 0, stdout.decode(), stderr.decode()
```

- [ ] **Step 3: Connect TUI to Installer**
Add an "Install" button or keybinding in `MatrixApp` that gathers selected cells and runs `asyncio.gather(*tasks)`.

- [ ] **Step 4: Commit**
```bash
git commit -am "feat: interactive matrix and parallel installation"
```

---

### Task 5: Hybrid Mode (TUI File Picker)

**Files:**
- Modify: `src/apk_installer/tui.py`
- Modify: `src/apk_installer/cli.py`

- [ ] **Step 1: Add directory/file selection to TUI**
If no APKs passed via CLI, use Textual's DirectoryTree to let users select files.

- [ ] **Step 2: Final cleanup and docs**
Update README.md with installation instructions.
