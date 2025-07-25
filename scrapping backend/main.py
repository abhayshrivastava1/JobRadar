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




driver = launch_driver(
    browser="chrome",  # or "edge"
    user_data_dir=r"D:\whatsapp-bot-profile",
    driver_path=r"C:\Users\Acer\AppData\Roaming\Python\Python312\site-packages\chromedriver_py\chromedriver_win64.exe"
)

# ✅ Load WhatsApp
print("✅ Launching WhatsApp Web...")
driver.get("https://web.whatsapp.com")

print("🔓 Waiting for WhatsApp Web to load...")
WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
print("✅ WhatsApp Web loaded.\n")



all_filtered, all_manual = scrape_groups(driver, GROUP_NAMES, WAIT_TIME, MAX_MESSAGES)


# ✅ Step 2: Scrape WhatsApp Channels
# for channel_url in CHANNEL_LINKS:
#     print(f"\n📡 Scanning channel: {channel_url}")
#     try:
#         messages = get_messages_from_channel(driver, channel_url, MAX_MESSAGES)
#         filtered, manual = classify_messages(messages)

#         all_filtered.extend(filtered)
#         all_manual.extend(manual)
#     except Exception as e:
#         print(f"❌ Failed to scrape {channel_url}: {e}")
#         continue



channel_filtered, channel_manual = scrape_channels(driver, CHANNEL_LINKS, MAX_MESSAGES)
all_filtered.extend(channel_filtered)
all_manual.extend(channel_manual)


# after scraping is complete:
enrich_and_export(all_filtered, all_manual, LOCATION_KEYWORDS)

print("\n✅ Done scanning all groups.")
driver.quit()