from itertools import count
import requests
from bs4 import BeautifulSoup
import json

raw_url = "https://suspilne.media/latest/?page="
urls_list = []
data = []

for num in range(1, 100):
    url = f"{raw_url}{num}"
    urls_list.append(url)

gen_id = count(1)

for url in urls_list:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_=lambda div: div in {"c-article-card__content", "c-article-card-bgimage__content"})
        for article in articles:
            headline = article.find("span", class_=lambda span: span in {"c-article-card__headline-inner", "c-article-card-bgimage__headline-inner"}) 
            if headline:
                headline = headline.text.strip()

            link_tag = article.find("a", class_=lambda a: a in {"c-article-card__headline", "c-article-card-bgimage__headline"})
            if link_tag:
                link = link_tag["href"]

            time_tag = article.find("time", class_=lambda time: time in {"c-article-card__info__time", "c-article-card-bgimage__info__time"})
            if time_tag:
                datetime = time_tag["datetime"]

            id = next(gen_id)
            meta = {
                "id": id,
                "headline": headline,
                "url": link,
                "time": datetime
            }
            data.append(meta)
    else:
        print("Failed to fetch")

with open("./data/bs4_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)