from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
import time
import pyautogui
import json

PATH_TO_chromedriver = "/Users/cna/chromedriver_mac_arm64/chromedriver"  # Replace with path to ChromeDriver

driver = webdriver.Chrome()
url = f"https://gemini.google.com/?hl=en"

driver.get(url)

print("Waiting for page to load...")
driver.quit()
