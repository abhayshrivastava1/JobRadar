# scraper.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from filter import classify_messages
from group_utils import get_messages_from_group  

def scrape_groups(driver, group_names, wait_time, max_messages):
    all_filtered = []
    all_manual = []

    for group_name in group_names:
        print(f" Opening group: {group_name}")

        try:
            # Wait for search bar
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.click()
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            time.sleep(1)

            # Search and open group
            search_box.send_keys(group_name)
            time.sleep(2)
            group = driver.find_element(By.XPATH, f'//span[@title="{group_name}"]')
            group.click()
            time.sleep(2)
        except:
            print(f"❌ Group '{group_name}' not found or not clickable.")
            continue

        # Get and classify messages
        messages = get_messages_from_group(driver, wait_time, max_messages)
        filtered, manual = classify_messages(messages)

        all_filtered.extend(filtered)
        all_manual.extend(manual)

    return all_filtered, all_manual
