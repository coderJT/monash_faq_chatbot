import subprocess
import sys

def install_playwright_browsers():
    try:
        # Only install if not already installed
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--with-deps"],
            check=True
        )
        print("✅ Playwright browsers installed.")
    except subprocess.CalledProcessError as e:
        print("Failed to install Playwright browsers:", e)

if __name__ == "__main__":
    install_playwright_browsers()
