# %%
# Imports and setting up Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import undetected_chromedriver as uc

# I used this module to store my email and pword
# This is not on the github
from pwordProtect import Protection

# Initialize undetected ChromeDriver
driver = uc.Chrome(version_main=128)

# Open the Suno website
driver.get("https://suno.com/")
time.sleep(random.uniform(1, 5))

# Simulate a random mouse movement
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
# TODO: Google login sometimes asks to verify that its your account if IP isn't recognized. Not sure a fix for that

#%%
# Optional cell to close driver after opening
driver.close()
# %%
