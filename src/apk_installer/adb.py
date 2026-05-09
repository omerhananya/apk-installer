"""ADB utility functions for interacting with Android Debug Bridge."""

import subprocess
import shutil
from dataclasses import dataclass


@dataclass
class Device:
    """Represents an Android device."""

    serial: str
    status: str
    model: str


def check_adb_exists() -> bool:
    """Check if 'adb' executable is available in the system PATH.

    Returns:
        bool: True if adb is found, False otherwise.
    """
    return shutil.which("adb") is not None


def get_adb_version() -> str:
    """Get the version of the installed ADB.

    Returns:
        str: The first line of 'adb --version' output, or an empty string if adb is not found or fails.
    """
    try:
        return subprocess.check_output(["adb", "--version"], text=True).splitlines()[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_devices() -> list[Device]:
    """Get a list of connected Android devices using 'adb devices -l'.

    Returns:
        list[Device]: A list of Device objects.
    """
    try:
        output = subprocess.check_output(["adb", "devices", "-l"], text=True)
        devices = []
        lines = output.strip().splitlines()
        if not lines:
            return []

        # Skip "List of devices attached"
        for line in lines[1:]:
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            serial = parts[0]
            status = parts[1]
            model = "unknown"

            # Search for model:<model> in the rest of the parts
            for part in parts[2:]:
                if part.startswith("model:"):
                    model = part.split(":", 1)[1]
                    break

            devices.append(Device(serial=serial, status=status, model=model))

        return devices
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
