import os
import sys
import platform
import subprocess
import shutil

def clean_build_dirs():
    """Remove previous build artifacts."""
    for d in ["build", "dist"]:
        if os.path.exists(d):
            shutil.rmtree(d)
    
    for f in os.listdir("."):
        if f.endswith(".spec"):
            os.remove(f)
            
    print("Cleaned previous build artifacts.")

def build():
    """Run PyInstaller to build the executable."""
    system = platform.system()
    print(f"Detected System: {system}")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "Maze Runner",
        "--clean",
        "--hidden-import", "psycopg2",
        "--hidden-import", "pygame",
        "main.py"
    ]
    
    if system == "Darwin":
        print("Building for macOS...")
        # macOS specific additions (icon, bundle identifier, etc could be added here)
        # cmd.extend([
        #     "--target-arch", "universal2", # Removed to avoid "not a fat binary" error if dependencies aren't universal
        # ])
        
    elif system == "Windows":
        print("Building for Windows...")
        
    elif system == "Linux":
        print("Building for Linux...")
    
    print(f"Running command: {' '.join(cmd)}")
    
    env = os.environ.copy()
    env["PYINSTALLER_CONFIG_DIR"] = os.path.join(os.getcwd(), "build", "cache")
    
    try:
        subprocess.check_call(cmd, env=env)
        print("\nBuild Complete!")
        
        # Copy .env file to the build directory
        if os.path.exists(".env"):
            if system == "Darwin":
                # For macOS .app bundle
                dest_dir = os.path.join("dist", "Maze Runner.app", "Contents", "MacOS")
                shutil.copy(".env", os.path.join(dest_dir, ".env"))
                print(f"Copied .env to {dest_dir}")
            else:
                # For Windows/Linux onedir
                dest_dir = os.path.join("dist", "Maze Runner")
                if system == "Windows":
                    dest_dir = os.path.join("dist", "Maze Runner") # Redundant but clear
                shutil.copy(".env", os.path.join(dest_dir, ".env"))
                print(f"Copied .env to {dest_dir}")
        else:
            print("Warning: .env file not found. The app might not connect to the database.")

        if system == "Darwin":
            print(f"App Bundle: dist/Maze Runner.app")
            print("To run: open 'dist/Maze Runner.app'")
        elif system == "Windows":
            print(f"Executable: dist\\Maze Runner\\Maze Runner.exe")
        elif system == "Linux":
            print(f"Executable: dist/Maze Runner/Maze Runner")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    clean_build_dirs()
    build()
