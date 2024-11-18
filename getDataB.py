# CONTINUOUS WORKFLOW FOR BEATOVEN

# LOGIN VIA GOOGLE + SETUP WEBDRIVER
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import undetected_chromedriver as uc
import chromedriver_binary
import requests
import re
from pydub import AudioSegment
from io import BytesIO
import convertFile

import sys
import threading
import time

# Global event to control the spinner
stop_spinner = threading.Event()

# Spinner function with explicit control
def spinner():
    symbols = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_spinner.is_set():  # Stop when the event is set
        sys.stdout.write("\r" + "Loading " + symbols[idx])
        sys.stdout.flush()
        idx = (idx + 1) % len(symbols)
        time.sleep(0.1)
    sys.stdout.write("\r")  # Clear the line when done

# Function to start the spinner
def start_loading(description):
    global stop_spinner
    stop_spinner.clear()  # Reset the stop event
    print(f"\nStarting {description}...")
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    return spinner_thread

# Function to stop the spinner
def stop_loading(spinner_thread, description):
    global stop_spinner
    stop_spinner.set()  # Signal the spinner to stop
    spinner_thread.join()  # Wait for the spinner to fully stop
    print(f"{description} COMPLETED")


# I used this module to store my email and pword
# This is not on the github
from pwordProtect import Protection

options = uc.ChromeOptions()
#options.add_argument("--headless=new")  # Headless mode

# Initialize undetected
driver = uc.Chrome(options=options)

def login():
    spinner_thread = start_loading("LOGIN")
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
    stop_loading(spinner_thread, "LOGIN FINISHED")

def create(q=None):
    # CREATE SONG 
    driver.get("https://sync.beatoven.ai/workspace")
    time.sleep(random.uniform(1,3))
    # Locate the textarea element using its class or placeholder
    textarea = driver.find_element(By.XPATH, '//textarea[@placeholder="Describe the music that you want. You can include duration, vibe, era and occasion."]')

    # Clear any existing text (if needed) and send the prompt
    textarea.clear()  # This step is optional if you want to clear the textarea first
    if q==None:
        # SINGLE CASE
        QUERY = input("What kind of song do you want? Include duration, vibe, era, etc: ")
    else:
        # BULK CASE
        QUERY = q

    textarea.send_keys(QUERY)

    time.sleep(random.uniform(3,6))

    # Locate the button using its class or text (you can use either method)
    compose_button = driver.find_element(By.XPATH, '//button[contains(text(), "Compose Music")]')

    # Click the button to trigger the action
    compose_button.click()

    spinner_thread = start_loading("CREATION (will take 60 seconds)")
    time.sleep(random.uniform(60,65))
    stop_loading(spinner_thread, "CREATION FINISHED")

    # TAKES A LITTLE WHILE TO BE CREATED

def download():
    spinner_thread = start_loading("DOWNLOAD")
    
    # Step 1: Locate the button with the descriptive file name
    file_name_button = driver.find_element(By.CLASS_NAME, 'btn-rename')
    file_name = file_name_button.text.strip()  # Extract and clean up the file name text

    # Step 2: Locate the audio element and extract the src URL
    audio_element = driver.find_element(By.TAG_NAME, 'audio')
    audio_url = audio_element.get_attribute('src')

    # Step 3: Download the audio file using the requests library
    response = requests.get(audio_url)
    if response.status_code != 200:
        stop_loading(spinner_thread, "DOWNLOAD")
        print(f"Failed to download audio file: Status code {response.status_code}")
        return

    # Optional: Save the downloaded AAC file locally for debugging
    aac_file_name = f"{file_name.replace(' ', '_')}.aac"
    with open(aac_file_name, "wb") as f:
        f.write(response.content)

    # Step 4: Convert the AAC file (downloaded in memory) to MP3
    try:
        convertFile.convert_aac_to_mp3(aac_file_name)
        print(f"Audio file '{aac_file_name}' downloaded and converted to MP3 successfully.")
    except Exception as e:
        print(f"Error during AAC to MP3 conversion: {e}")
    finally:
        stop_loading(spinner_thread, "DOWNLOAD FINISHED")

def clear():
    spinner_thread = start_loading("CLEARING WORKSPACE (for unlimited creations)")
    driver.get("https://sync.beatoven.ai/workspace")
    # Wait up to 10 seconds for the <p> element to be visible
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'My Projects')]"))
    )
    element.click()

    time.sleep(6)
    # Locate all main buttons for created songs
    song_buttons = driver.find_elements(By.CLASS_NAME, "btn-project-tile")
    time.sleep(2)

    # Loop through each song button
    for song_button in song_buttons:
        # Locate the subbutton inside each song button and click it to open the dropdown
        subbutton = song_button.find_element(By.CLASS_NAME, "bg-kebab")
        subbutton.click()
        
        # Small delay to ensure the dropdown loads
        time.sleep(1)

        # Locate the "Delete" button in the dropdown and click it
        delete_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Delete')]")
        delete_button.click()
        
        # Small delay to handle any confirmation dialog, if present
        time.sleep(1)

    stop_loading(spinner_thread, "WORKSPACE CLEARED")

def bulk_create_and_download(QUERY_LIST):
    counter = 1
    for query in QUERY_LIST:
        print(f"STARTING DOWNLOAD NUMBER: {counter}")
        create(query)
        download()
        clear()
        counter+=1


def main():
    if input("Ready to log in? (y/n): ") == "y":
        login()
    else:
        driver.close()

    while input("Do you want another song? (y/n): ") != "n":
        create()
        download()
        clear()
    
    # Will start with 3 songs in the batch
    batch = [
        "Compose a 30-second track for a bachelor party. The music should complement the lively and celebratory atmosphere of the event.",
        "Compose a 30-second track for a bachelorette party. The music should enhance the joyful and fun occasion.",
        "Compose a 30-second track for a yoga session. The music should align with the calming and focused nature of the activity.",
        "Compose a 30-second track for a weightlifting session. The music should match the intense and dynamic energy of the workout."
        ]  
    
    if input("Do you want a batch query? (y/n): ") == "y":
        print("Okay, here is your batch list: ")
        print(batch)
        bulk_create_and_download(batch)
        time.sleep(3)
    
    
    print("ENDING SESSION")
    driver.close()

main()
