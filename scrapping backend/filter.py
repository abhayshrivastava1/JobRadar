import re
import requests
from bs4 import BeautifulSoup
from config import LOCATION_KEYWORDS  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def contains_location(text):
    text = text.lower()
    matched = [loc for loc in LOCATION_KEYWORDS if loc.lower() in text]
    if matched:
        print(f" Matched location(s): {matched}")
    return bool(matched), matched


def extract_link(text):
    url_pattern = r'https?://[^\s<>)"\']+'
    matches = re.findall(url_pattern, text)
    return matches[0] if matches else ""


def page_contains_location(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.get_text().lower()

        found, matched_keywords = contains_location(page_text)
        if found:
            print(f" MATCH FOUND in page: {matched_keywords}")
        return found, matched_keywords

    except Exception as e:
        print(f" Selenium Error for {url}:\n{e}")
        return False, []


def classify_messages(messages):
    filtered = []
    manual = []

    #  Initialize headless Chrome ONCE
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    driver = webdriver.Chrome(options=chrome_options)

    for msg in messages:
        print(f"\n Checking message:\n{msg}")
        found_in_msg, msg_keywords = contains_location(msg)
        if found_in_msg:
            filtered.append((msg, f"location-found-directly: {msg_keywords}"))
        else:
            link = extract_link(msg)
            print(f" Extracted link: {link}")
            if link:
                found_in_link, link_keywords = page_contains_location(link, driver)
                if found_in_link:
                    filtered.append((msg, f"location-found-in-link: {link_keywords}"))
                else:
                    print(" No keyword found in message or link — adding to manual")
                    manual.append((msg, "no-location"))
            else:
                print(" No link found — adding to manual")
                manual.append((msg, "no-location"))

    #  Quit only once
    driver.quit()
    return filtered, manual

