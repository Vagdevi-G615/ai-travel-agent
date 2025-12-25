import requests
from bs4 import BeautifulSoup
import os
import time

OUTPUT_DIR = "knowledge_base"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

WIKIVOYAGE = "https://en.wikivoyage.org/wiki/"
WIKIPEDIA = "https://en.wikipedia.org/wiki/"

THEME_PAGES = {
    "adventure": [
        "Adventure_travel",
        "Trekking",
        "Scuba_diving",
        "Mountaineering"
    ],
    "solo": [
        "Solo_travel_(tourism)",
        "Personal_safety",
        "Backpacking"
    ],
    "budget": [
        "Budget_travel",
        "Hostels",
        "Public_transport"
    ],
    "eco": [
        "Ecotourism",
        "Sustainable_tourism"
    ],
    "luxury": [
        "Luxury_travel",
        "Resort",
        "Boutique_hotel"
    ]
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find("div", class_="mw-parser-output")

    if not content:
        return ""

    text = ""
    for p in content.find_all("p"):
        para = p.get_text().strip()
        if len(para) > 40:  # ✅ LOWERED THRESHOLD
            text += para + "\n\n"

    return text

def fetch_page(page):
    print(f"Trying Wikivoyage: {page}")
    text = extract_text(WIKIVOYAGE + page)

    if len(text.strip()) < 200:
        print(f"↪ Falling back to Wikipedia: {page}")
        text = extract_text(WIKIPEDIA + page)

    time.sleep(1)
    return text

for theme, pages in THEME_PAGES.items():
    print(f"\n📘 Building knowledge for theme: {theme}")
    theme_text = ""

    for page in pages:
        theme_text += fetch_page(page)

    file_path = f"{OUTPUT_DIR}/{theme}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(theme_text)

    print(f"✅ Saved: {file_path} ({len(theme_text)} chars)")

print("\n🎉 Knowledge base successfully built!")
