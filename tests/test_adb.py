from unittest.mock import patch
import pytest
from apk_installer.adb import check_adb_exists, get_adb_version, get_devices, Device

def test_check_adb_exists_true():
    with patch("shutil.which", return_value="/usr/local/bin/adb"):
        assert check_adb_exists() is True

def test_check_adb_exists_false():
    with patch("shutil.which", return_value=None):
        assert check_adb_exists() is False

def test_get_adb_version_success():
    mock_output = "Android Debug Bridge version 1.0.41\nVersion 34.0.4-10411375\nInstalled as /opt/android-sdk/platform-tools/adb"
    with patch("subprocess.check_output", return_value=mock_output):
        assert get_adb_version() == "Android Debug Bridge version 1.0.41"

def test_get_adb_version_failure():
    with patch("subprocess.check_output", side_effect=FileNotFoundError):
        assert get_adb_version() == ""

def test_get_devices_success():
    mock_output = (
        "List of devices attached\n"
        "emulator-5554          device product:sdk_gphone64_arm64 model:sdk_gphone64_arm64 device:emulator64_arm64 transport_id:1\n"
        "0123456789ABCDEF       device usb:1-1 product:redfin model:Pixel_5 device:redfin transport_id:2\n"
    )
    with patch("subprocess.check_output", return_value=mock_output):
        devices = get_devices()
        assert len(devices) == 2
        assert devices[0].serial == "emulator-5554"
        assert devices[0].status == "device"
        assert devices[0].model == "sdk_gphone64_arm64"
        assert devices[1].serial == "0123456789ABCDEF"
        assert devices[1].status == "device"
        assert devices[1].model == "Pixel_5"

def test_get_devices_empty():
    mock_output = "List of devices attached\n"
    with patch("subprocess.check_output", return_value=mock_output):
        devices = get_devices()
        assert devices == []

def test_get_devices_missing_model():
    mock_output = (
        "List of devices attached\n"
        "emulator-5554          device product:sdk_gphone64_arm64 device:emulator64_arm64 transport_id:1\n"
    )
    with patch("subprocess.check_output", return_value=mock_output):
        devices = get_devices()
        assert len(devices) == 1
        assert devices[0].serial == "emulator-5554"
        assert devices[0].model == "unknown"

def test_get_devices_called_process_error():
    import subprocess
    with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "adb")):
        devices = get_devices()
        assert devices == []
