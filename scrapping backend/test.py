# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# driver_path = r"C:\Users\Acer\AppData\Roaming\Python\Python312\site-packages\chromedriver_py\chromedriver_win64.exe"

# options = Options()
# options.add_argument(r"user-data-dir=D:\whatsapp-bot-profile")
# # ❌ REMOVE this line completely if present:
# # options.add_argument("profile-directory=Profile 4")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-blink-features=AutomationControlled")



# driver = webdriver.Chrome(service=Service(driver_path), options=options)
# driver.get("https://web.whatsapp.com/channel/0029Va9mu8Z8PgsD51mVDT04")

# WebDriverWait(driver, 60).until(
#     EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
# )

# print("✅ WhatsApp Web is ready!")


# # Keep the browser open so the channel has time to load
# input("🟢 WhatsApp is open. Press ENTER to exit...\n")
# driver.quit()


# Temporary test
from config import LOCATION_KEYWORDS

def contains_location(text):
    text = text.lower()
    print(f"Keywords: {LOCATION_KEYWORDS}")
    return any(loc.lower() in text for loc in LOCATION_KEYWORDS)

print(contains_location("Urgent hiring in Noida"))  # should be True
print(contains_location("Work from home only"))     # should be False


# def get_messages_from_channel(driver, channel_url, max_messages):
#     driver.get(channel_url)
#     print(f"🔗 Opening channel: {channel_url}")

#     try:
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]'))
#         )
#     except:
#         print("❌ Channel did not load.")
#         return []

#     messages = set()
#     last_height = driver.execute_script("return document.body.scrollHeight")
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

