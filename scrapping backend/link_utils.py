# link_utils.py
import re
import requests
from readability import Document
from bs4 import BeautifulSoup

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
