import json
from pathlib import Path
base_path = Path(__file__).parent.parent

with open(base_path / "./data/dataset.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

wdiff = []
for article in articles:
    lemma_tone = article["lemma_compound_tone"]
    stem_tone = article["stem_compound_tone"]
    if (lemma_tone == stem_tone):
        print(article["id"])
    else:
        wdiff.append(article)

with open(base_path / "./data/wdiff_dataset.json", "w", encoding="utf-8") as file:
    json.dump(wdiff, file, ensure_ascii=False, indent=4)

print(f"Total differing entries: {len(wdiff)}")