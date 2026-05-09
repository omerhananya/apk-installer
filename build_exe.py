import PyInstaller.__main__
import os
import sys

def build():
    print("🚀 Building standalone executable...")
    
    # Define the entry point
    entry_point = os.path.join("apk_installer", "cli.py")
    
    # PyInstaller arguments
    args = [
        entry_point,
        "--onefile",
        "--name=apk-installer",
        "--clean",
        # Textual needs some special handling sometimes, 
        # but usually its CSS is bundled automatically if it's in the package
    ]
    
    PyInstaller.__main__.run(args)
    
    print(f"\n✅ Build complete! Check the 'dist/' folder for the binary.")

if __name__ == "__main__":
    build()
