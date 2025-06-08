import os
import subprocess
import platform
import sys

def is_git_repo():
    return os.path.isdir('.git')

def update_repo():
    print("🔄 Checking for updates from GitHub...")
    try:
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("⚠️ Git pull failed:", result.stderr)
    except Exception as e:
        print(f"❌ Error running git pull: {e}")

def start_app():
    python_cmd = 'python'
    if platform.system() != 'Windows':
        python_cmd = 'python3'

    print("🚀 Starting study.py...")
    try:
        subprocess.call([python_cmd, 'study.py'])
    except Exception as e:
        print(f"❌ Failed to start study.py: {e}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if not is_git_repo():
        print("❌ This folder is not a Git repository. Make sure you cloned it via git.")
        sys.exit(1)

    update_repo()
    start_app()

if __name__ == "__main__":
    main()
