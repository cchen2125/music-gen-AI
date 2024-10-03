# %%
# Imports and setting up Webdriver
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
import random
from datetime import datetime
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from pwordProtect import Protection

# Set up Chrome options 
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration. It's recommended to use this option.
chrome_options.add_argument("--window-size=1920,1080")  # Optional: Set a specific window size.
chrome_options.add_argument("--disable-extensions")  # Disables extensions.
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model.
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems.

# Initialize the Chrome WebDriver
#driver = webdriver.Chrome(service=Service(), options=chrome_options)

# Initialize undetected ChromeDriver
driver = uc.Chrome(version_main=128)

# Open the Suno website
driver.get("https://suno.com/")

# Simulate human-like delays between actions
time.sleep(random.uniform(1, 5))

# Simulate a random mouse movement (this won't be as effective but can help)
actions = webdriver.ActionChains(driver)
actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()

# Get taken to login screen
time.sleep(random.uniform(1, 5))
driver.get("https://suno.com/create")

# %%
# Go to google login and simulate login workflow
time.sleep(random.uniform(1, 5))
google_button = driver.find_element(By.CLASS_NAME, 'cl-socialButtonsIconButton__google')
google_button.click()
time.sleep(random.uniform(1, 5))

# Name and pword [stored in Protected module for privacy]
EMAIL = Protection.name
PASSWORD = Protection.password

# Add email and password
driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(EMAIL)
driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
time.sleep(random.uniform(3,6))
driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
time.sleep(random.uniform(10,13))

# %%
# TODO: Once logged in, need a method of verifying accounts with phone (if needed)
# TODO: This one might just have to be manual

#%%
# Optional cell to close driver after opening
driver.close()
# %%
