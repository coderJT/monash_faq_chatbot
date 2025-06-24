import streamlit as st
import subprocess
import sys
import os

# Ensure Playwright browsers are installed.
# This block runs once when the app starts up.
# It checks if the browsers are already installed to avoid redundant operations.
try:
    # A simple check if the 'browsers' directory exists in the playwright cache path
    # You might need a more robust check depending on your Playwright version
    # You can also run `playwright install` and check its output for "already installed"
    playwright_browsers_path = os.path.join(
        os.path.expanduser("~/.cache/ms-playwright"),
        "chromium-1234", # Example, actual version changes
        "chrome-linux"   # Or firefox-linux, webkit-linux
    )
    # Better: just run install and let playwright decide if it's already installed
    st.info("Ensuring Playwright browsers are installed...")
    install_command = [sys.executable, "-m", "playwright", "install"]

    # Capture output to check for "browsers are already installed"
    result = subprocess.run(install_command, capture_output=True, text=True, check=False)

    if result.returncode == 0:
        if "browsers are already installed" in result.stdout:
            st.success("✅ Playwright browsers are already installed.")
        else:
            st.success("✅ Playwright browsers installed successfully!")
    else:
        st.error(f"❌ Failed to install Playwright browsers. Error: {result.stderr}")
        st.stop() # Stop the app if installation fails critically

except Exception as e:
    st.error(f"❌ An unexpected error occurred during Playwright browser setup: {e}")
    st.stop() # Stop the app if there's an issue with the setup process

# --- Your main Streamlit app code starts here ---

from playwright.sync_api import sync_playwright

def run_playwright_task():
    st.write("Running Playwright task...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch() # Ensure headless=True (default)
            page = browser.new_page()
            page.goto("https://example.com")
            title = page.title()
            browser.close()
            st.success(f"Page title: {title}")
    except Exception as e:
        st.error(f"Error during Playwright task: {e}")

st.title("Playwright Demo on Streamlit Cloud")

if st.button("Run Playwright Task"):
    run_playwright_task()