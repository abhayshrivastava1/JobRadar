# exporter.py

import os
import re
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from readability import Document
import pandas as pd



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


def ensure_all_keys_filtered(data_list, column_order_filtered):
    for entry in data_list:
        for key in column_order_filtered:
            if key not in entry:
                entry[key] = [] if key == "Matched Keywords" else "N/A"
    return data_list


def ensure_all_keys_manual(data_list, column_order_manual):
    for entry in data_list:
        for key in column_order_manual:
            if key not in entry:
                # entry[key] = [] if key == "MatchedKeywords" else "N/A"
                continue
    return data_list


def enrich_and_export(all_filtered, all_manual, LOCATION_KEYWORDS):
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    column_order_filtered = ["Message", "Link", "Page Content", "Matched Keywords"]
    column_order_manual = ["Message", "Link", "Page Content"]


    filtered_data = []
    manual_data = []
    seen_links = set()
    # skipped_manual = []


    for msg, _ in all_filtered:

        if msg.strip().startswith("+91"):
            continue

        link = extract_link(msg)
        page_text = get_page_text(link) if link else "N/A"

        if link == "N/A" or page_text == "N/A":
            continue

        combined_text = (msg + " " + page_text).lower()
        matched_keywords = [kw for kw in LOCATION_KEYWORDS if kw.lower() in combined_text]

        entry = {
            "Message": msg,
            "Link": link,
            "Page Content": page_text,
            "Matched Keywords": matched_keywords
        }

        if matched_keywords:
            # filtered_data.append(entry)
            if link not in seen_links:   # duplicate check
                filtered_data.append(entry)
                seen_links.add(link)
                
        else:
            # entry.pop("Matched Keywords", None)  
            # manual_data.append(entry)
            entry.pop("Matched Keywords", None)  
            if link not in seen_links:   # duplicate check
                manual_data.append(entry)
                seen_links.add(link)

        

    for msg, _ in all_manual:

        if msg.strip().startswith("+91"):
            continue

        link = extract_link(msg)
        page_text = get_page_text(link) if link else "N/A"

        if link == "N/A" or page_text == "N/A":
            # skipped_manual.append({
            #     "Message": msg,
            #     "Link": link,
            #     "Page Content": page_text
            # })
            continue

        combined_text = (msg + " " + page_text).lower()
        # matched_keywords = [kw for kw in LOCATION_KEYWORDS if kw.lower() in combined_text]

        entry = {
            "Message": msg.strip().replace("\n", " ").strip(),
            "Link": link,
            "Page Content": page_text,
            
        }

        # manual_data.append(entry)
        if link not in seen_links:   # duplicate check
            manual_data.append(entry)
            seen_links.add(link)

    # Ensure consistency
    filtered_data = ensure_all_keys_filtered(filtered_data, column_order_filtered)
    manual_data = ensure_all_keys_manual(manual_data, column_order_manual)

    # Clean manual_data (Matched Keywords hatao agar reh gaya ho)
    for entry in manual_data:
        entry.pop("Matched Keywords", None)



    # Write CSV
    # filtered_filename = "../local backend/output/filtered_jobs.csv"
    # manual_filename = "../local backend/output/manual_review.csv"

    # Current file (scrapping backend/exporter.py) ka folder
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Project root (JobRadar)
    PROJECT_ROOT = os.path.dirname(BASE_DIR)

    # Local backend/output
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, "local backend", "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filtered_filename = os.path.join(OUTPUT_DIR, f"filtered_jobs_{timestamp}.csv")
    manual_filename   = os.path.join(OUTPUT_DIR, f"manual_review_{timestamp}.csv")



    # Use respective column orders
    with open(filtered_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=column_order_filtered)
        writer.writeheader()
        writer.writerows(filtered_data)


    with open(manual_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=column_order_manual)
        writer.writeheader()
        writer.writerows(manual_data)


    # Also save as DataFrame with respective columns
    # pd.DataFrame(filtered_data)[column_order_filtered].to_csv(filtered_filename, index=False, encoding="utf-8")
    # pd.DataFrame(manual_data)[column_order_manual].to_csv(manual_filename, index=False, encoding="utf-8")

    # Safe export
    if filtered_data:
        pd.DataFrame(filtered_data)[column_order_filtered].to_csv(filtered_filename, index=False, encoding="utf-8")
    else:
        pd.DataFrame(columns=column_order_filtered).to_csv(filtered_filename, index=False, encoding="utf-8")

    if manual_data:
        pd.DataFrame(manual_data)[column_order_manual].to_csv(manual_filename, index=False, encoding="utf-8")
    else:
        pd.DataFrame(columns=column_order_manual).to_csv(manual_filename, index=False, encoding="utf-8")



    print(f" Total messages scanned: {len(filtered_data) + len(manual_data)}")
    print(f" Filtered:               {len(filtered_data)}")
    print(f" Manual:                 {len(manual_data)}")
   


    return filtered_filename, manual_filename