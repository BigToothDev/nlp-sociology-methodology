from pathlib import Path
import pandas as pd
import json
from nltk.stem.snowball import SnowballStemmer
base_path = Path(__file__).parent.parent

with open(base_path / "./data/tone-dict-uk.tsv", "r", encoding="utf-8") as file:
    tonedict = pd.read_csv(file, sep="\t", names=["word", "score"])

with open(base_path / "./data/bs4_data_lemma.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

stemmer = SnowballStemmer("russian") # Ukrainian is not available

stemtonedict = {}
for _, row in tonedict.iterrows():
    stem = stemmer.stem(row["word"])
    score = float(row["score"])
    stemtonedict[stem] = score

for article in articles:
    headline_lemma = article["headline_lemma"]
    words = headline_lemma.split()
    stem_words = [stemmer.stem(word) for word in words]
    article["headline_stem_of_lemma"] = " ".join(stem_words)

with open(base_path / "./data/tone-dict-uk-stem.json", "w", encoding="utf-8") as file:
    json.dump(stemtonedict, file, ensure_ascii=False, indent=4)

with open(base_path / "./data/bs4_data_stem.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)