# Suno continous workflow
"""
Login with Microsoft instead of Google to support manual creation
of Microsoft account with Sterneworks domain

Microsoft accounts created so far:
- Robert
- John

"""

# Imports and setting up Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import undetected_chromedriver as uc
import requests
import re
from pwordProtect import Protection
import sys
import threading
import time

# Initialize undetected
#NUM_DRIVERS = len(Protection.sterne_names)
NUM_DRIVERS = 2 # need to make more microsoft accounts

active_drivers = []
version = 130

for i in range(NUM_DRIVERS):
    active_drivers.append(uc.Chrome(version_main=version))

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

# Sleep helper function with randomness
def random_sleep(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))


def login():
    spinner_thread = start_loading("LOGIN")
    # Open the Suno website
    for i, driver in enumerate(active_drivers):
        # Protected module for email and password
        EMAIL = Protection.sterne_names[i]
        PASSWORD = Protection.sterne_pwords[i]

        # Go to Suno page
        driver.get('http://suno.com/create')

        # Go to Microsoft login and simulate login workflow
        random_sleep(1, 5)
        microsoft_button = driver.find_element(By.CLASS_NAME, 'cl-socialButtonsIconButton__microsoft')
        microsoft_button.click()

        # Wait for the email input field to appear and fill in the email
        random_sleep(3, 6)
        email_input = driver.find_element(By.ID, 'i0116')
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)  # Simulate pressing Enter

        # Wait for the password input field to appear and fill in the password
        random_sleep(3, 6)
        password_input = driver.find_element(By.ID, 'i0118')
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.RETURN)  # Simulate pressing Enter
        stop_loading(spinner_thread, f"LOGIN FINISHED FOR DRIVER {i+1}")

        # Click next when given the stay signed in option
        try:
            decline_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'declineButton'))
            )
            decline_button.click()  # Click "No" to decline staying signed in
        except Exception as e:
            print(f"Error bypassing 'Stay signed in?' prompt: {e}")

    # Allow time for the login process to complete
    random_sleep(10, 15)

def create(q=None):
    for driver in active_drivers:
        driver.get('http://suno.com/create')

        if q==None:
            # SINGLE CASE
            QUERY = input("What kind of song do you want? Include duration, vibe, era, etc: ")
        else:
            # BULK CASE
            QUERY = q

        query_field = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]/div[2]/div/div/textarea')
        query_field.send_keys(QUERY)

        random_sleep(3,6)

        create_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/div/div[3]/div[3]/button')
        create_btn.click()

    # Suno creation takes between 2 and 3 mins (give 3 mins for creation)
    spinner_thread = start_loading("CREATION (will take up to 180 seconds)")
    random_sleep(160,170)
    stop_loading(spinner_thread, "CREATION FINISHED")

# Helper function for download (cleaning the text)
def cleanText(full_text):
    # Define markers
    start_marker = "[Verse]"
    end_marker = "Edit Displayed Lyrics"

    # Extract lyrics between the markers
    if start_marker in full_text and end_marker in full_text:
        start_index = full_text.find(start_marker)
        end_index = full_text.find(end_marker)
        lyrics_text = full_text[start_index:end_index].strip()
    else:
        lyrics_text = "Lyrics not found or improperly formatted."
    return lyrics_text

def download():
    spinner_thread = start_loading("DOWNLOAD")

    for i, driver in enumerate(active_drivers):
        driver.get('http://suno.com/me')
        random_sleep(3,6)

        account = Protection.sterne_names[i].split('@')[0]

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

        NUM_SONGS = 2 # since 2 songs are created for each creation

        for i in range(NUM_SONGS):
            driver.get(song_hrefs[i])
            time.sleep(2)
            # Wait for the correct play button to be present and clickable
            play_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "text-vinylBlack-darker") and @type="button"]'))
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

                #print(audio_element)
                
                # Get the 'src' attribute from the audio element
                audio_url = audio_element.get_attribute("src")
                
                # Print the audio URL to verify
                print("Audio URL:", audio_url)
                
                if audio_url:
                    # Download the audio file using requests
                    response = requests.get(audio_url)
                    file_name = f"{song_titles[i]}_v{i+1}_{account}.mp3"
                    
                    # Save the audio file
                    with open(file_name, "wb") as file:
                        file.write(response.content)
                    
                    print(f"Downloaded: {file_name}")
                else:
                    print("Audio URL not found.")

            except Exception as e:
                print(f"An error occurred downloading audio: {e}")
            
            try:
                # Locate the textarea and extract the text
                textarea = driver.find_element(By.CLASS_NAME, 'relative.overflow-y-hidden')
                text_content = textarea.get_attribute('value')

                # If text is inside the tag's inner content instead of 'value'
                if not text_content:
                    text_content = textarea.text

                text_content = cleanText(text_content)

                # Save the text to a .txt file
                file_path = f"{song_titles[i]}_v{i+1}_{account}.txt"
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_content)

                print(f"Text saved successfully to {file_path}")

            except Exception as e:
                print(f"An error occurred when downloading lyrics: {e}")
    
    stop_loading(spinner_thread, "DOWNLOAD FINISHED")

def bulk_create_and_download(QUERY_LIST):
    if len(QUERY_LIST)>5:
        print("MAX OF 50 CREDITS!!")
        return
    
    counter = 1
    for query_key in QUERY_LIST:
        print(f"STARTING DOWNLOAD NUMBER: {counter} / {len(QUERY_LIST)}")
        create(QUERY_LIST[query_key])
        download()
        counter+=1


def main():
    if input("Ready to login? (y/n): ") == "y":
        login()
        print("You are now logged in")
    else:
        for d in active_drivers:
            d.close()
        return

    batch = {'yoga': "Compose a track for a yoga session. The music should align with the calming and focused nature of the activity.",
        'weightlifting': "Compose a track for a weightlifting session. The music should match the intense and dynamic energy of the workout."
        }

    if input("Do you want a batch query? (y/n): ") == "y":
        print("Okay, here is your batch list: ")
        print(batch)
        bulk_create_and_download(batch)
        time.sleep(3)

    while input("Do you want another song? (y/n): ") != "n":
        create()
        download()


    print("ENDING SESSION")
    for driver in active_drivers:
        driver.close()
    return

main()