import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from dotenv import load_dotenv

# ─── Config & Constants ────────────────────────────────────────────────────────
load_dotenv()  # Load environment variables from .env file

UNIS_TAG = "NAU"
SPEED_TEST_URL = "https://www.speedtest.net/"
X_URL = "https://x.com/home"

# ENVIRONMENT VARIABLES
X_EMAIL = os.getenv("X_EMAIL")
X_PASSWORD = os.getenv("X_PASSWORD")
X_USERNAME = os.getenv("X_USERNAME")

if not X_EMAIL or not X_PASSWORD:
    raise ValueError("Please set the X_EMAIL and X_PASSWORD environment variables.")

# ─── Setup Selenium ─────────────────────────────────────────────────────────────
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# ─── Selenium Selectors ─────────────────────────────────────────────────────────
LOGIN_BUTTON_XPATH = (
    By.XPATH,
    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
)
USERNAME_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
)
PASSWORD_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
)
X_POST_INPUT_XPATH = (
    By.XPATH,
    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div'
)
X_POST_BUTTON = (
    By.XPATH,
    '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button'
)
SPEED_TEST_GO_BUTTON = (By.XPATH, '//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div/div[2]/a')
DOWNLOAD_SPEED_ELEMENT = (By.CSS_SELECTOR, "span.download-speed")
UPLOAD_SPEED_ELEMENT = (By.CSS_SELECTOR, "span.upload-speed")


# ─── Internet Speed Bot Class ───────────────────────────────────────────────────
class InternetSpeedTwitterBot:
    def __init__(self):
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        driver.get(SPEED_TEST_URL)
        driver.maximize_window()
        time.sleep(1)

        # Start speed test
        go_button = wait.until(EC.element_to_be_clickable(SPEED_TEST_GO_BUTTON))
        go_button.click()
        time.sleep(50)  # Wait for test to complete

        # Retrieve speed results
        try:
            self.down = wait.until(EC.presence_of_element_located(DOWNLOAD_SPEED_ELEMENT)).text
            self.up = wait.until(EC.presence_of_element_located(UPLOAD_SPEED_ELEMENT)).text
            print(f"Download Speed: {self.down} Mbps")
            print(f"Upload Speed: {self.up} Mbps")
        except NoSuchElementException:
            print("Speed test results not found.")

    def tweet_at_provider(self):
        driver.get(X_URL)
        driver.maximize_window()

        post_message = f"Hey @{UNIS_TAG}, why is my internet {self.down} Mbps download / {self.up} Mbps upload when I pay for more?"

        # Log in
        try:
            login_button = wait.until(EC.element_to_be_clickable(LOGIN_BUTTON_XPATH))
            login_button.click()
            login_button.send_keys(X_EMAIL)
            login_button.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            print("Login button not found.")
            return

        # Handle unusual login (if required)
        try:
            username_input = wait.until(EC.presence_of_element_located(USERNAME_INPUT_XPATH))
            username_input.send_keys(X_USERNAME)
            username_input.send_keys(Keys.RETURN)
            time.sleep(1)
            print("Handled unusual login prompt.")
        except TimeoutException:
            print("No unusual login prompt.")

        # Enter password
        try:
            password_input = wait.until(EC.element_to_be_clickable(PASSWORD_INPUT_XPATH))
            password_input.click()
            password_input.send_keys(X_PASSWORD)
            password_input.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print("Password input not found")

        # Write and post tweet
        try:
            post_input = wait.until(EC.element_to_be_clickable(X_POST_INPUT_XPATH))
            post_input.click()
            post_input.send_keys(post_message)
        except NoSuchElementException:
            print("Post input not found")

        try:
            post_button = wait.until(EC.element_to_be_clickable(X_POST_BUTTON))
            post_button.click()
            time.sleep(1)
        except NoSuchElementException:
            print("Post button not found")


# ─── Run the Bot ───────────────────────────────────────────────────────────────
bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
time.sleep(2)
bot.tweet_at_provider()
