import sys
from apk_installer.adb import check_adb_exists

def main():
    if not check_adb_exists():
        print("Error: 'adb' not found in PATH.", file=sys.stderr)
        print(
            "Please install Android Platform Tools: https://developer.android.com/tools/releases/platform-tools",
            file=sys.stderr,
        )
        sys.exit(1)
    print("ADB found. Ready.")

if __name__ == "__main__":
    main()
