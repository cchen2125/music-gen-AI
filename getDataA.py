# FULL WORKFLOW FOR LOGGING IN, CREATING, AND DOWNLOADING SONGS FROM SUNO.AI
# %%
# Imports and setting up Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import undetected_chromedriver as uc
import requests
import re

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
# Create song (CODE FROM download.ipynb)

driver.get('http://suno.com/create')

# CHANGE QUERY HERE 
QUERY = 'british rap song about having to navigate the 21st century as an old school person'

query_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]/div[2]/div/div/textarea')
query_field.send_keys(QUERY)

create_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]/div[3]/button')
create_btn.click()

time.sleep(random.uniform(18,28)) # May need to adjust

# %%
# Downloading created song from library

driver.get('http://suno.com/me')

time.sleep(random.uniform(4,7))

# Find all song elements on the page
song_elements = driver.find_elements(By.CSS_SELECTOR, 'div.w-full.flex.items-center.gap-1 a[href^="/song/"]')
song_titles = []

for el in song_elements:
    try:
        # Navigate to the parent span of the a tag
        parent_span = el.find_element(By.XPATH, '..')

        # Extract the title attribute from the parent span, which contains the song title
        song_title = parent_span.get_attribute("title")
        
        # Clean up the song title for use in filenames (optional)
        song_title_clean = re.sub(r'[\\/*?:"<>|]', "", song_title)  # Remove invalid filename characters

        song_titles.append(song_title_clean)
    except:
        continue

song_hrefs = [element.get_attribute('href') for element in song_elements]

NUM_SONGS = 2

for i in range(NUM_SONGS):
    driver.get(song_hrefs[i])
    time.sleep(2)
    # Wait for the correct play button to be present and clickable
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.chakra-button.css-1m4tiqz[aria-label="Play Count"]'))
    )
    play_button.click()
    time.sleep(1) 
    play_button.click()
    time.sleep(1) 

    try:
        # Wait for the audio element to be present and visible
        audio_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "active-audio-play"))
        )

        print(audio_element)
        
        # Get the 'src' attribute from the audio element
        audio_url = audio_element.get_attribute("src")
        
        # Print the audio URL to verify
        print("Audio URL:", audio_url)
        
        if audio_url:
            # Download the audio file using requests
            response = requests.get(audio_url)
            file_name = f"{song_titles[i]}.mp3"
            
            # Save the audio file
            with open(file_name, "wb") as file:
                file.write(response.content)
            
            print(f"Downloaded: {file_name}")
        else:
            print("Audio URL not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


#%%
# Optional cell to close driver after opening
driver.close()

# %%
