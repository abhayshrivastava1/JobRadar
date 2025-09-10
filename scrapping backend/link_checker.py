import requests
from bs4 import BeautifulSoup
from config import LOCATION_KEYWORDS

def check_link_for_location(url):
    try:
        response = requests.get(url, timeout=5)
        text = BeautifulSoup(response.text, 'html.parser').get_text()
        return any(loc.lower() in text.lower() for loc in LOCATION_KEYWORDS)
    except:
        return False