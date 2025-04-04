from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
from pathlib import Path
base_path = Path(__file__).parent.parent

with open(base_path / "./data/bs4_data_stem.json", "r", encoding="utf-8") as file:
   articles = json.load(file)

with open(base_path / "./data/tone-dict-uk-lemma.json", "r", encoding="utf-8") as file:
   lemma_tonedict = json.load(file)

with open(base_path / "./data/tone-dict-uk-stem.json", "r", encoding="utf-8") as file:
   stem_tonedict = json.load(file)

SIA_lemma = SentimentIntensityAnalyzer()
SIA_lemma.lexicon.update(lemma_tonedict)

SIA_stem = SentimentIntensityAnalyzer()
SIA_stem.lexicon.update(stem_tonedict)

for article in articles:
  headline_lemma = article["headline_lemma"]
  headline_stem_of_lemma = article["headline_stem_of_lemma"]
  lemma_ps = SIA_lemma.polarity_scores(headline_lemma)
  stem_ps = SIA_stem.polarity_scores(headline_stem_of_lemma)
  article["lemma_neg_tone"] = lemma_ps["neg"]
  article["lemma_neu_tone"] = lemma_ps["neu"]
  article["lemma_pos_tone"] = lemma_ps["pos"]
  article["lemma_compound_tone"] = lemma_ps["compound"]
  article["stem_neg_tone"] = stem_ps["neg"]
  article["stem_neu_tone"] = stem_ps["neu"]
  article["stem_pos_tone"] = stem_ps["pos"]
  article["stem_compound_tone"] = stem_ps["compound"]

with open(base_path / "./data/dataset.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)