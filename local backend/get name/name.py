from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def preprocess(text):
    # basic cleaning
    text = text.replace("|", " ")
    text = text.replace("-", " ")
    text = text.replace("—", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)  # multiple spaces -> single space
    return text.strip()

def extract_company(text):
    text = preprocess(text)

    # 1. "X is hiring"
    match = re.search(r"\b([\w&.\-]+(?:\s+[\w&.\-]+)*)\s+is hiring", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # 2. "at X" → multi-word capture
    match = re.search(r"\bat\s+([A-Za-z0-9&.\- ]+?)(?:\s+for|\s+\||$)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return "Unknown"

@app.route("/extract", methods=["POST"])
def extract():
    data = request.json
    text = data.get("text", "")
    company = extract_company(text)
    return jsonify({"company": company})

if __name__ == "__main__":
    app.run(debug=True, port=8000)


