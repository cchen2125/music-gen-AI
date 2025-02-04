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
        PASSWORD = Protection.sterne_pwords[i].capitalize()

        driver.get('https://www.stableaudio.com/')

        random_sleep(1, 3)
        login_btn = driver.find_element(By.XPATH, '/html/body/div/header/div/div/div[1]/button[2]')
        login_btn.click()

        random_sleep(2, 5)
        email_input = driver.find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[1]/div/div[1]/div/input')
        email_input.send_keys(EMAIL)

        random_sleep(2, 5)
        pwd_input = driver.find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[1]/div/div[2]/div/input')
        pwd_input.send_keys(PASSWORD)
        pwd_input.send_keys(Keys.RETURN)

        stop_loading(spinner_thread, f"LOGIN FINISHED FOR DRIVER {i+1}")

    random_sleep(10, 15)



def create(q=None):
    return


def download():
    return


def bulk_create_and_download(QUERY_LIST):
    return


def main():
    if input("Ready to login? (y/n): ") == "y":
        login()
        print("You are now logged in")
    else:
        for d in active_drivers:
            d.close()
        return

    # batch = {'yoga': "Compose a track for a yoga session. The music should align with the calming and focused nature of the activity.",
    #     'weightlifting': "Compose a track for a weightlifting session. The music should match the intense and dynamic energy of the workout."
    #     }

    # if input("Do you want a batch query? (y/n): ") == "y":
    #     print("Okay, here is your batch list: ")
    #     print(batch)
    #     bulk_create_and_download(batch)
    #     time.sleep(3)

    # while input("Do you want another song? (y/n): ") != "n":
    #     create()
    #     download()


    print("ENDING SESSION")
    for driver in active_drivers:
        driver.close()
    return

main()