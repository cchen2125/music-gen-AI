# FULL WORKFLOW FOR BEATOVEN.AI
# Songs are made quicker - so easier to do make and download in same setting

# %%
# LOGIN VIA GOOGLE + SETUP WEBDRIVER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import undetected_chromedriver as uc
import requests
import re
from pydub import AudioSegment
from io import BytesIO

# I used this module to store my email and pword
# This is not on the github
from pwordProtect import Protection

# Initialize undetected ChromeDriver
driver = uc.Chrome(version_main=128)

# Open the Suno website
driver.get('https://sync.beatoven.ai/')
time.sleep(random.uniform(1, 5))

# Simulate a random mouse movement
actions = webdriver.ActionChains(driver)
actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()

# Get taken to login screen
# Locate the 'Sign in with Google' button by the form action or button class
google_signin_button = driver.find_element(By.XPATH, '//button[span[text()="Sign in with Google"]]')
google_signin_button.click()
time.sleep(random.uniform(3, 7))

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
# CREATE SONG 

# Locate the textarea element using its class or placeholder
textarea = driver.find_element(By.XPATH, '//textarea[@placeholder="Describe the music that you want. You can include duration, vibe, era and occasion."]')

# Clear any existing text (if needed) and send the prompt
textarea.clear()  # This step is optional if you want to clear the textarea first
textarea.send_keys("I want a 30 second rap song about trying to get into university with a modern vibe.")

time.sleep(random.uniform(3,6))

# Locate the button using its class or text (you can use either method)
compose_button = driver.find_element(By.XPATH, '//button[contains(text(), "Compose Music")]')

# Click the button to trigger the action
compose_button.click()

# TAKES A LITTLE WHILE TO BE CREATED

# %%
# DOWNLOAD SONG (song page opened)

# Step 1: Locate the button with the descriptive file name
file_name_button = driver.find_element(By.CLASS_NAME, 'btn-rename')
file_name = file_name_button.text.strip()  # Extract and clean up the file name text

# Step 2: Locate the audio element and extract the src URL
audio_element = driver.find_element(By.TAG_NAME, 'audio')
audio_url = audio_element.get_attribute('src')

# Step 3: Download the audio file using the requests library
response = requests.get(audio_url)

# Step 4: Convert the AAC file (downloaded in memory) to MP3
file_name_clean = file_name.replace(' ', '_')  # Clean the file name
audio_file_name = f"{file_name_clean}.mp3"  # Save the final file as MP3

# Step 5: Load the AAC file directly from the response content (in-memory)
aac_audio = AudioSegment.from_file(BytesIO(response.content), format="aac")

# Step 6: Export the audio as an MP3 file
aac_audio.export(audio_file_name, format="mp3")

print(f"Audio file '{audio_file_name}' downloaded and converted to MP3 successfully.")
# %%
driver.close()
# %%
