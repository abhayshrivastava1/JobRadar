import os
import re
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from readability import Document
from config import LOCATION_KEYWORDS


def extract_link(text):
    match = re.search(r'(https?://\S+)', text)
    return match.group(0) if match else ""


def get_page_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200:
            doc = Document(response.text)
            main_html = doc.summary()
            soup = BeautifulSoup(main_html, "html.parser")
            return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f" Error reading page: {url}\n{e}")
    return "N/A"


def save_results(all_filtered):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filtered_data = []
    manual_data = []

    for msg, _ in all_filtered:
        link = extract_link(msg)
        page_text = get_page_text(link) if link else "N/A"

        entry = {
            "Message": msg,
            "Link": link,
            "PageContent": page_text
        }

        combined_text = (msg + " " + page_text).lower()
        if any(keyword.lower() in combined_text for keyword in LOCATION_KEYWORDS):
            filtered_data.append(entry)
        else:
            manual_data.append(entry)

    df_filtered = pd.DataFrame(filtered_data)
    df_manual = pd.DataFrame(manual_data)



    # Current file (scrapping backend/exporter.py ya jo bhi run ho raha hai) ka parent folder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Project root (JobRadar)
    PROJECT_ROOT = os.path.dirname(BASE_DIR)

    # Local backend/output
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "local backend", "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # filtered_filename = os.path.join(OUTPUT_DIR, "filtered_jobs.csv")
    # manual_filename = os.path.join(OUTPUT_DIR, "manual_review.csv")
    filtered_filename = os.path.join(OUTPUT_DIR, f"filtered_jobs_{timestamp}.csv")
    manual_filename   = os.path.join(OUTPUT_DIR, f"manual_review_{timestamp}.csv")



    df_filtered.to_csv(filtered_filename, index=False, encoding="utf-8")
    df_manual.to_csv(manual_filename, index=False, encoding="utf-8")

    print(f" Filtered data saved to: {filtered_filename}")
    print(f" Manual review data saved to: {manual_filename}")
