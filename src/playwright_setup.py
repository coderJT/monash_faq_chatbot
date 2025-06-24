import subprocess
import sys
import os

def install_playwright():
    cache_path = os.path.expanduser("~/.cache/ms-playwright")
    if not os.path.exists(os.path.join(cache_path, "chromium")):
        print("🔧 Installing Playwright browsers...")
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    else:
        print("✅ Playwright browsers already installed.")

# Run on import
install_playwright()