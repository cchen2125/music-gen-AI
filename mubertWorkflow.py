# Imports and setting up Webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
from pwordProtect import Protection
import sys
import threading
import time
from selenium.webdriver.chrome.options import Options

"""
TODO:
1) Create more Sterneworks facebook/mubert accounts
2) Change the way the name is downloaded (since Mubert doesn't create track names)
3) Test with multiple WDs
"""

# Initialize undetected
#NUM_DRIVERS = len(Protection.sterne_names)
NUM_DRIVERS = 1 # need to make more microsoft accounts

active_drivers = []
version = 132


for i in range(NUM_DRIVERS):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled") # bypass recaptcha
    driver = webdriver.Chrome(options=options)  # Regular ChromeDriver initialization
    active_drivers.append(driver)

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

    for i, driver in enumerate(active_drivers):
        # Protected module for email and password
        EMAIL = Protection.sterne_names[i]
        PASSWORD = Protection.sterne_pwords[i]

        # Go to Mubert page (sign up page to bypass recaptcha)
        driver.get('https://mubert.com/render/sign-up')

        # Go to Microsoft login and simulate login workflow

        actions = webdriver.ActionChains(driver)
        actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
        random_sleep(3, 6)
        
        facebook_button = driver.find_element(By.XPATH, "//button[.//div[text()='Login with Facebook']]")
        facebook_button.click()

        # Wait for the email input field to appear and fill in the email

        actions = webdriver.ActionChains(driver)
        actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
        random_sleep(3, 6)
        email_input = driver.find_element(By.ID, 'email')
        email_input.send_keys(EMAIL)

        # Wait for the password input field to appear and fill in the password
        actions = webdriver.ActionChains(driver)
        actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
        random_sleep(3, 6)
        password_input = driver.find_element(By.ID, 'pass')
        password_input.send_keys(PASSWORD)

        # Simulate a random mouse movement
        actions = webdriver.ActionChains(driver)
        actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
        random_sleep(2,4)
        password_input.send_keys(Keys.RETURN)  # Simulate pressing Enter

        random_sleep(5, 8)
        continue_button = driver.find_element(By.XPATH, "//div[@aria-label[contains(., 'Continue as')]]")
        continue_button.click()

        stop_loading(spinner_thread, f"LOGIN FINISHED FOR DRIVER {i+1}")

    # Allow time for the login process to complete
    random_sleep(10, 15)

def create(q=None):
    # CREATE SONG 
    for driver in active_drivers:
        driver.get("https://mubert.com/render?authBy=facebook#_=_")
        random_sleep(3,6)

        # Locate the textarea element using its class or placeholder
        textarea = driver.find_element(By.XPATH, "//textarea[@name='prompt']")

        # Clear any existing text (if needed) and send the prompt
        textarea.clear()  # This step is optional if you want to clear the textarea first
        if q==None:
            # SINGLE CASE
            QUERY = input("What kind of song do you want? Include duration, vibe, era, etc: ")
        else:
            # BULK CASE
            QUERY = q

        textarea.send_keys(QUERY)

        random_sleep(3,6)

        # Locate the button using its class or text (you can use either method)
        compose_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        # Click the button to trigger the action
        compose_button.click()
        spinner_thread = start_loading("CREATION (will take 60 seconds)")
        time.sleep(random.uniform(60,65))
        stop_loading(spinner_thread, "CREATION FINISHED")

        # TAKES A LITTLE WHILE TO BE CREATED


def download():
    spinner_thread = start_loading("DOWNLOAD")

    for i, driver in enumerate(active_drivers):
        driver.get('https://mubert.com/render/my-generated-tracks')
        random_sleep(3,6)

        account = Protection.sterne_names[i].split('@')[0]

        song_titles = []
        song_hrefs = []

        
        # Find all <a> elements inside the divs
        track_links = driver.find_elements(By.CSS_SELECTOR, ".track-name-dropdown__wrapper a.track-name")

        # Extract both href and text (song title)
        for link in track_links:
            href = link.get_attribute("href")  # Get full track URL
            song_hrefs.append(href)
            song_title = link.text.strip()  # Extract and clean song title text
            if len(song_title)>0:
                song_titles.append(song_title)


        print("Songs Found:", song_titles)
        print("Song URLs:", song_hrefs)

        NUM_SONGS = 1 # since 2 songs are created for each creation

        # Loop through each track URL
        for i in range(NUM_SONGS):
            driver.get(song_hrefs[i])
            time.sleep(5) 

            try:
                # Locate the <audio> element
                audio_element = driver.find_element(By.TAG_NAME, "audio")
                mp3_url = audio_element.get_attribute("src")

                if mp3_url:
                    print(f"MP3 Found: {mp3_url}")

                    # Extract file name from URL
                    file_name = f"songs/mubert/{song_titles[i]}_v{i+1}_{account}.mp3"

                    # Download MP3
                    response = requests.get(mp3_url, stream=True)
                    with open(file_name, "wb") as file:
                        file.write(response.content)

                    print(f"Downloaded: {file_name}")

            except Exception as e:
                print("No audio element found:", e)
    
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
    batch = {
    "pride_month": "Compose a track celebrating Pride Month. The music should be vibrant, uplifting, and embody themes of love, unity, and LGBTQ+ pride.",
    "black_history_month": "Compose a track celebrating Black History Month. The music should reflect pride, resilience, and cultural heritage.",
    }

    login()

    if input("Do you want a batch query? (y/n): ") == "y":
        print("Okay, here is your batch list: ")
        print(batch)
        bulk_create_and_download(batch)
        time.sleep(3)

    print("ENDING SESSION")
    for driver in active_drivers:
        driver.close()

main()