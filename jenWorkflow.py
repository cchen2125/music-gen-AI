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

NUM_DRIVERS = 1

active_drivers = []
version = 132

for i in range(NUM_DRIVERS):
    account = Protection.sterne_names[i].split('@')[0]

    chromeOptions = uc.ChromeOptions()
    prefs = {"download.default_directory" : f"/Users/clarachen/Documents/Harvard/Radcliffe Research Partners/music-gen-AI/jen/{account}"}
    chromeOptions.add_experimental_option("prefs",prefs)

    active_drivers.append(uc.Chrome(version_main=version, options=chromeOptions))

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
    print(f'\nStarting {description}...')
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

        driver.get('https://app.jenmusic.ai/login')

        # Go to Facebook log in and simulate login workflow

        actions = webdriver.ActionChains(driver)
        actions.move_by_offset(random.randint(10, 50), random.randint(10, 50)).perform()
        random_sleep(3, 6)
        
        facebook_button = driver.find_element(By.XPATH, '//button[contains(@class, "fvaui-button-web3auth")]//span[text()="Facebook"]')
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
    for driver in active_drivers:
        if q==None:
            # SINGLE CASE
            QUERY = input("What kind of song do you want? Include duration, vibe, era, etc: ")
        else:
            # BULK CASE
            QUERY = q

        query_field = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div/div[4]/form/div[2]/div/div[2]/div[2]/div[3]/div/div[3]/div[2]/div[1]/textarea')
        query_field.clear()
        query_field.send_keys(QUERY)

        random_sleep(1,2)

        generate_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div/div[4]/form/div[2]/div/div[2]/div[3]/button')
        generate_btn.click()

    spinner_thread = start_loading("CREATION (will take up to 60 seconds)")
    random_sleep(50, 60)
    stop_loading(spinner_thread, "CREATION FINISHED")

    return


def download():
    spinner_thread = start_loading("DOWNLOAD")

    for driver in active_drivers:

        latest_song = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div/div[2]/div/div[3]/div[1]')
        latest_song.click()

        download_btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[2]/div/div[3]/div[2]/div/div/div/div[1]/div[1]/div[2]/div[1]')
        download_btn.click()

        random_sleep(1, 2)

    random_sleep(1, 3)

    stop_loading(spinner_thread, "DOWNLOAD FINISHED")
    return


def bulk_create_and_download(QUERY_LIST):
    if len(QUERY_LIST)>20:
        print("MAX OF 20 SONGS PER MONTH!!")
        return

    counter = 1
    for query_key in QUERY_LIST:
        print(f"STARTING DOWNLOAD NUMBER: {counter} / {len(QUERY_LIST)}")
        create(QUERY_LIST[query_key])
        download()
        counter+=1
    return


def main():
    if input("Ready to login? (y/n): ") == "y":
        login()
        print("You are now logged in")
    else:
        for d in active_drivers:
            d.close()
        return
    
    batch = {
        "indigenous_ceremony": "Compose a track for an Indigenous ceremony. The music should respect traditional rhythms and cultural significance.",
        "lunar_new_year": "Compose a cheerful, upbeat track for celebrating lunar new year"
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

        