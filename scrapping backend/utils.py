import re

def extract_links(text):
    return re.findall(r'(https?://[^\s]+)', text)