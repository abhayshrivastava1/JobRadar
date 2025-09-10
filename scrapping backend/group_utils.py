from selenium.webdriver.common.by import By
import time

def get_messages_from_group(driver, wait_time, max_messages):
    time.sleep(wait_time)

    collected_texts = set()
    last_count = 0
    scroll_attempts = 20  # Max times to scroll up
    scroll_pause = 1.5  # Pause between scrolls

    for _ in range(scroll_attempts):
        # Step 1: Collect all current messages
        message_elements = driver.find_elements(
            By.XPATH,
            '//div[contains(@class, "message-in") or contains(@class, "message-out")]//div[@class and not(@class="copyable-text")]'

        )

        for el in message_elements:
            text = el.text.strip()
            if text:
                collected_texts.add(text)

        # Step 2: Check if we reached the message limit
        if len(collected_texts) >= max_messages:
            break

        # Step 3: Scroll up to load older messages
        try:
            chat_container = driver.find_element(By.XPATH, '//div[@data-testid="chat-history"]')
            driver.execute_script("arguments[0].scrollTop = 0", chat_container)
            
        except Exception as e:
            print(f" Scroll error: {e}")
            break

        time.sleep(scroll_pause)

        # Step 4: Stop if no new messages were added after scroll
        if len(collected_texts) == last_count:
            print("🔚 No new messages loaded — stopping scroll.")
            break

        last_count = len(collected_texts)

    print(f" Total messages collected from group: {len(collected_texts)}")
    return list(collected_texts)[-max_messages:]
