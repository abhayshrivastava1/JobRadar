from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import CHANNEL_LINKS
from filter import classify_messages
from channel_utils import get_messages_from_channel



# def get_messages_from_channel(driver, channel_url, max_messages=30):
#     driver.get(channel_url)
#     print(f"🔗 Opening channel: {channel_url}")

#     # ⏳ Wait until messages appear
#     try:
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]'))
#         )
#     except:
#         print("❌ Channel did not load.")
#         return []

#     messages = set()
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     # ✅ Optimized XPath
#     xpath = '//div[@role="listitem"]//span[@dir="auto" and string-length(normalize-space(text())) > 0]'

#     while len(messages) < max_messages:
#         try:
#             elements = driver.find_elements(By.XPATH, xpath)
#             for el in elements:
#                 try:
#                     txt = el.text.strip()
#                     if txt:
#                         messages.add(txt)
#                         if len(messages) >= max_messages:
#                             break
#                 except Exception as e:
#                     print(f"⚠️ Error reading element: {e}")
#                     continue

#             # 🔻 Scroll down
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(8)

#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 print("📉 Reached end of messages.")
#                 break
#             last_height = new_height

#         except Exception as e:
#             print(f"❌ Error scraping: {e}")
#             break

#     print(f"✅ Scraped {len(messages)} messages.")
#     return list(messages)[:max_messages]


# channel_scraper.py
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from filter import classify_messages
from channel_utils import get_messages_from_channel

def scrape_channels(driver, channel_urls, max_messages):
    all_filtered = []
    all_manual = []

    for url in channel_urls:
        print(f"\n📺 Scraping channel: {url}")
        try:
            messages = get_messages_from_channel(driver, url, max_messages)
            filtered, manual = classify_messages(messages)

            all_filtered.extend(filtered)
            all_manual.extend(manual)

        except Exception as e:
            print(f"❌ Error with channel {url}: {e}")
            continue

    return all_filtered, all_manual
