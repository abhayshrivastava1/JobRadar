from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import CHANNEL_LINKS
from filter import classify_messages
from channel_utils import get_messages_from_channel

def scrape_channels(driver, channel_urls, max_messages):
    all_filtered = []
    all_manual = []

    for url in channel_urls:
        print(f"\n Scraping channel: {url}")
        try:
            messages = get_messages_from_channel(driver, url, max_messages)
            filtered, manual = classify_messages(messages)

            all_filtered.extend(filtered)
            all_manual.extend(manual)

        except Exception as e:
            print(f" Error with channel {url}: {e}")
            continue

    return all_filtered, all_manual