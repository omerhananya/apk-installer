from unittest.mock import patch
from apk_installer.adb import check_adb_exists, get_adb_version

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
