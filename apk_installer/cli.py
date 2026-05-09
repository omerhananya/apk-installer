import sys

from apk_installer.adb import check_adb_exists, get_devices
from apk_installer.tui import FilePickerApp, MatrixApp


def main():
    """CLI entry point for apk-installer."""
    if not check_adb_exists():
        print("Error: 'adb' not found in PATH.", file=sys.stderr)
        print(
            "Please install Android Platform Tools: https://developer.android.com/tools/releases/platform-tools",
            file=sys.stderr,
        )
        sys.exit(1)

    # Extract APK files from arguments
    apks = [arg for arg in sys.argv[1:] if arg.endswith(".apk")]

    if not apks:
        # Launch file picker TUI
        picker = FilePickerApp()
        apks = picker.run()
        if not apks:
            return

    # Get connected devices
    devices = get_devices()
    if not devices:
        print("No Android devices found via ADB.")
        return

    # Launch the selection matrix TUI
    app = MatrixApp(apks, devices)
    app.run()


if __name__ == "__main__":
    main()
