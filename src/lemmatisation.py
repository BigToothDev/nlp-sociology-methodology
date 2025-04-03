import spacy
from pathlib import Path
import json

nlp = spacy.load("uk_core_news_trf")
base_path = Path(__file__).parent.parent

with open(base_path / "./data/bs4_data_clean.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

for article in articles:
    lemma = nlp(article["headline_clean"])
    article["headline_lemma"] = " ".join([token.lemma_ for token in lemma])

with open(base_path / "./data/bs4_data_lemma.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)