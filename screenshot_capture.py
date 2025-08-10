"""
Screenshot capture script for LawGPT interface
This script opens the application in a browser and captures a screenshot
"""

import time
import subprocess
import os
from selenium import webdriver
from selenium import __version__ as selenium_version
from selenium.webdriver.chrome.options import Options

def capture_screenshot():
    try:
        print("📸 Starting screenshot capture process...")
        
        # Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1200,800')
        
        # Initialize Chrome driver
        print("🌐 Opening Chrome browser...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the application
        print("🔗 Navigating to LawGPT interface...")
        driver.get('http://localhost:5000')
        
        # Wait for the page to load
        time.sleep(3)
        
        # Take screenshot
        screenshot_path = os.path.join(os.getcwd(), 'lawgpt_interface.png')
        driver.save_screenshot(screenshot_path)
        print(f"✅ Screenshot saved: {screenshot_path}")
        
        # Close browser
        driver.quit()
        
        return screenshot_path
        
    except Exception as e:
        print(f"❌ Error capturing screenshot: {e}")
        print("📝 Note: Make sure Chrome browser and ChromeDriver are installed")
        print("📝 Also ensure the Flask app is running on http://localhost:5000")
        return None

if __name__ == "__main__":
    # Check if Flask app is running
    try:
        import requests
        response = requests.get('http://localhost:5000', timeout=2)
        if response.status_code == 200:
            print("✅ Flask application is running")
            screenshot_path = capture_screenshot()
        else:
            print("❌ Flask application is not responding")
    except:
        print("❌ Flask application is not running")
        print("🚀 Please start the application with: python flask_app.py")
