from pathlib import Path
import re
import json
base_path = Path(__file__).parent.parent

with open(base_path / "./data/stopwords_ua_list.txt", "r", encoding="utf-8") as file:
    ua_stopwords = file.read()

def clean(data, stopwords):
    words = data.split()
    filtered_words = [word for word in words if word not in stopwords]
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", " ".join(filtered_words))).strip()

with open(base_path / "./data/bs4_data.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

for article in articles:
    content = article["headline"]
    clean_headline = clean(content, ua_stopwords)
    article["headline_clean"] = clean_headline

with open(base_path / "./data/bs4_data_clean.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)