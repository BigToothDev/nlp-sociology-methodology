from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from pathlib import Path
import pandas as pd
import json
import urllib.request

def load_json_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read().decode('utf-8-sig'))
    except Exception as e:
        print(f"Error loading data from {url}: {e}")
        return []

ds_url = "https://raw.githubusercontent.com/BigToothDev/nlp-sociology-methodology/refs/heads/main/data/dataset.json"
ds_diff_url = "https://raw.githubusercontent.com/BigToothDev/nlp-sociology-methodology/refs/heads/main/data/wdiff_dataset.json"

ds = load_json_from_url(ds_url)
ds_diff = load_json_from_url(ds_diff_url)

appdir = Path(__file__).parent.parent if "__file__" in globals() else Path.cwd()

app_ui = ui.page_fluid(
    ui.tags.link(href="styles.css", rel="stylesheet"),
    ui.panel_title("DataExplorer"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.div(
                ui.h6("Num of articles:"),
                ui.output_text("num_articles"),
                ui.br(),
                ui.input_switch("data_toggle", "Show only differing tone articles", value=False),
                ui.br(),
                ui.input_selectize("article_id", "Select an article by ID:", []),
                ui.br(),
                ui.input_text("keyword", "Search by keyword:", ""),
                ui.input_action_button("search_btn", "Find", class_="search_btn"),
                ui.br(),
                ui.br(),
                ui.input_selectize("article_id_search", "Articles matching keyword:", []),
                ui.input_action_button("clear_btn", "Clear Selection", class_="clear_btn"),
                class_="custom_side"
            )
        ),
        ui.div(
            ui.h3("Article Title:"),
            ui.output_text_verbatim("headline"),
            ui.h4("Date:"),
            ui.output_text_verbatim("datetime"),
            ui.h4("URL:"),
            ui.output_text_verbatim("link"),
            ui.h4("LEMMA, General sentiment:"),
            ui.output_text_verbatim("lemma_general_sentiment"),
            ui.h4("LEMMA, Tone of the article:"),
            ui.output_text_verbatim("lemma_tone"),
            ui.h4("STEM, General sentiment:"),
            ui.output_text_verbatim("stem_general_sentiment"),
            ui.h4("STEM, Tone of the article:"),
            ui.output_text_verbatim("stem_tone"),
            class_="custom_content"
        )
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def current_df():
        return pd.json_normalize(ds_diff if input.data_toggle() else ds)

    @output()
    @render.text
    def num_articles():
        return len(current_df())

    @reactive.Calc
    def select_article_by_id():
        article_id = input.article_id_search() or input.article_id()
        if article_id is None:
            return None
        filtered = current_df()[current_df()["id"] == int(article_id)]
        if not filtered.empty:
            return filtered.iloc[0].to_dict()
        return None

    @output()
    @render.text
    def headline():
        article = select_article_by_id()
        if article:
            return article.get('headline', "No headline available")
        return "No article selected"

    @output()
    @render.text
    def content():
        article = select_article_by_id()
        if article is not None:
            return article.get('content', "No content available")
        return "No article selected"

    @output()
    @render.text
    def link():
        article = select_article_by_id()
        if article is not None:
            return article.get('url', "")
        return ""

    @output()
    @render.text
    def datetime():
        article = select_article_by_id()
        if article is not None:
            return article.get('time', "")
        return ""

    @output()
    @render.text
    def lemma_tone():
        article = select_article_by_id()
        if article is not None:
            return f"Negative tone: {article.get('lemma_neg_tone', 'N/A')} | Neutral tone: {article.get('lemma_neu_tone', 'N/A')} | Positive tone: {article.get('lemma_pos_tone', 'N/A')} | Compound tone: {article.get('lemma_compound_tone', 'N/A')}"
        return ""

    @output()
    @render.text
    def stem_tone():
        article = select_article_by_id()
        if article is not None:
            return f"Negative tone: {article.get('stem_neg_tone', 'N/A')} | Neutral tone: {article.get('stem_neu_tone', 'N/A')} | Positive tone: {article.get('stem_pos_tone', 'N/A')} | Compound tone: {article.get('stem_compound_tone', 'N/A')}"
        return ""

    @output()
    @render.text
    def lemma_general_sentiment():
        article = select_article_by_id()
        if article is not None:
            compound_tone = article.get('lemma_compound_tone', 0)
            try:
                compound_tone = float(compound_tone)
                if compound_tone >= 0.05:
                    return "Positive"
                elif compound_tone <= -0.05:
                    return "Negative"
                else:
                    return "Neutral"
            except (ValueError, TypeError):
                return "Unknown"
        return ""

    @output()
    @render.text
    def stem_general_sentiment():
        article = select_article_by_id()
        if article is not None:
            compound_tone = article.get('stem_compound_tone', 0)
            try:
                compound_tone = float(compound_tone)
                if compound_tone >= 0.05:
                    return "Positive"
                elif compound_tone <= -0.05:
                    return "Negative"
                else:
                    return "Neutral"
            except (ValueError, TypeError):
                return "Unknown"
        return ""

    @reactive.effect
    @reactive.event(input.search_btn)
    def search_kw():
        keyword = input.keyword()
        if keyword:
            filtered_data = current_df()[current_df()['headline_lemma'].str.contains(keyword, case=False, na=False)]
            ui.update_selectize(
                session=session,
                id="article_id_search",
                choices=[str(id) for id in filtered_data['id']] if not filtered_data.empty else [],
            )
            ui.update_selectize(
                session=session,
                id="article_id",
                choices=[]
            )

    @reactive.effect
    def clear_selectize():
        if input.clear_btn():
            ui.update_selectize(
                session=session,
                id="article_id_search",
                choices=[]
            )
            ui.update_selectize(
                session=session,
                id="article_id",
                choices=[str(id) for id in current_df()["id"]]
            )
            ui.update_text(
                session=session,
                id="keyword",
                value=""
            )

    @reactive.effect
    def update_on_toggle():
        ui.update_selectize(
            session=session,
            id="article_id",
            choices=[str(id) for id in current_df()["id"]]
        )
        ui.update_selectize(
            session=session,
            id="article_id_search",
            choices=[]
        )

app = App(app_ui, server)
