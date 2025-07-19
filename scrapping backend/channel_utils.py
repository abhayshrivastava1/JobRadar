# channel_utils.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# def get_messages_from_channel(driver, channel_url, max_messages=30, scroll_attempts=10):
#     driver.get(channel_url)
#     print(f"🔗 Opening channel invite: {channel_url}")

#     try:
#         # ✅ Wait until redirected and the channel header appears
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'_amru')]"))
#         )
#         print("✅ Channel view loaded.")

#         # ✅ Find the scrollable container (usually with this class)
#         scrollable = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'_ak72')]"))
#         )

#         # ✅ Scroll UP to load older messages
#         for i in range(scroll_attempts):
#             driver.execute_script("arguments[0].scrollTop = 0", scrollable)
#             print(f"⬆️ Scrolled up [{i + 1}/{scroll_attempts}]")
#             time.sleep(2)

#         # ✅ Now collect messages
#         messages = driver.find_elements(By.XPATH, "//div[contains(@class,'_ak73')]")
#         print(f"💬 Total messages found: {len(messages)}")

#         extracted = []
#         for msg in messages[:max_messages]:
#             try:
#                 text = msg.text.strip()
#                 if text:
#                     extracted.append(text)
#             except:
#                 continue

#         return extracted

#     except Exception as e:
#         print(f"❌ Error loading channel: {e}")
#         return []


def get_messages_from_channel(driver, channel_url, max_messages=30):
    # 🔗 Step 1: Open the channel
    driver.get(channel_url)
    print(f"🔗 Opening channel: {channel_url}")

    # 🕒 Step 2: Wait for channel to load
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="listitem"]'))
        )
    except:
        print("❌ Channel did not load.")
        return []

    # 📦 Step 3: Initialize variables
    collected_texts = set()
    scroll_attempts = 100  # 🔁 Max scroll-ups
    scroll_pause = 1.5  # ⏸ Pause between scrolls
    last_count = 0

    # 📌 Step 4: Get scrollable chat container
    try:
        scroll_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.XPATH,
        '//div[@role="region" and @tabindex="0"]'
        ))
    )
    except Exception as e:
        print("❌ Unable to find scrollable container.")
        return []

    # ♻️ Step 5: Scroll up repeatedly and collect messages
    for attempt in range(scroll_attempts):
        # 🔍 5.1: Get all current visible messages
        try:
            message_elements = driver.find_elements(
                By.XPATH,
                '//div[@role="listitem"]//span[@dir="auto" and string-length(normalize-space(text())) > 0]'
            )
        except Exception as e:
            print(f"❌ Error finding message elements: {e}")
            break

        for el in message_elements:
            try:
                txt = el.text.strip()
                if txt:
                    collected_texts.add(txt)
                    if len(collected_texts) >= max_messages:
                        break
            except Exception as e:
                print(f"⚠️ Error reading message text: {e}")
                continue

        # ✅ 5.2: Stop if we have enough messages
        if len(collected_texts) >= max_messages:
            break

        # 🔼 5.3: Scroll up to load older messages
        try:
            driver.execute_script("arguments[0].scrollTop = 0", scroll_container)
        except Exception as e:
            print(f"⚠️ Scroll error: {e}")
            break

        time.sleep(scroll_pause)

        # 🧮 5.4: Stop if no new messages were loaded
        if len(collected_texts) == last_count:
            print("🔚 No new messages loaded — stopping scroll.")
            break

        last_count = len(collected_texts)

    # 📊 Step 6: Return the last N messages
    print(f"✅ Scraped {len(collected_texts)} messages from channel.")
    return list(collected_texts)[-max_messages:]

