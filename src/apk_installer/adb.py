"""ADB utility functions for interacting with Android Debug Bridge."""

import subprocess
import shutil


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
