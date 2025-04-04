import spacy
from pathlib import Path
import pandas as pd
import json

nlp = spacy.load("uk_core_news_trf")
base_path = Path(__file__).parent.parent

with open(base_path / "./data/tone-dict-uk.tsv", "r", encoding="utf-8") as file:
    tonedict = pd.read_csv(file, sep="\t", names=["word", "score"])

with open(base_path / "./data/bs4_data_clean.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

lemmatonedict = {}
for _, row in tonedict.iterrows():
    doc = nlp(row["word"])
    lemma = doc[0].lemma_
    score = float(row["score"])
    lemmatonedict[lemma] = score

for article in articles:
    lemma = nlp(article["headline_clean"])
    article["headline_lemma"] = " ".join([token.lemma_ for token in lemma])

with open(base_path / "./data/tone-dict-uk-lemma.json", "w", encoding="utf-8") as file:
    json.dump(lemmatonedict, file, ensure_ascii=False, indent=4)

with open(base_path / "./data/bs4_data_lemma.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)