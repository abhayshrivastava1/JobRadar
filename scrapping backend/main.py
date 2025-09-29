from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from group_utils import get_messages_from_group
from filter import classify_messages
from config import WAIT_TIME, MAX_MESSAGES, GROUP_NAMES, LOCATION_KEYWORDS, CHANNEL_CODES, CHANNEL_LINKS
from chromedriver_py import binary_path as driver_path
import re
import pandas as pd
from datetime import datetime
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
from readability import Document
from channel_scraper import get_messages_from_channel
from whatsapp_driver import launch_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from group_scraper import scrape_groups
from exporter import enrich_and_export
from channel_scraper import scrape_channels
from channel_utils import get_messages_from_channel
from csv_to_sqlite import get_latest_csv, import_csv_to_sqlite, CSV_FOLDER, CSV_PREFIXES, DB_PATH




driver = launch_driver(
    browser="chrome",  # or "edge"
    user_data_dir=r"D:\whatsapp-bot-profile",    
)

# Load WhatsApp
print(" Launching WhatsApp Web")
driver.get("https://web.whatsapp.com")

print(" Waiting for WhatsApp Web to load")
WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
print(" WhatsApp Web loaded.\n")



all_filtered, all_manual = scrape_groups(driver, GROUP_NAMES, WAIT_TIME, MAX_MESSAGES)


channel_filtered, channel_manual = scrape_channels(driver, CHANNEL_LINKS, MAX_MESSAGES)
all_filtered.extend(channel_filtered)
all_manual.extend(channel_manual)


# after scraping is complete:
filtered_filename, manual_filename = enrich_and_export(all_filtered, all_manual, LOCATION_KEYWORDS)

import_csv_to_sqlite(filtered_filename, DB_PATH)
import_csv_to_sqlite(manual_filename, DB_PATH)


print("\n Done scanning all groups.")
driver.quit()