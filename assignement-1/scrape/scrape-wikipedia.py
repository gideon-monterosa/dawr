from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

WIKI_URL = 'https://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Graub%C3%BCnden'

def scrape_gemeinden():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(WIKI_URL)
        page.wait_for_load_state('networkidle')

        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')

        data = []
        rows = soup.select('table.wikitable tbody tr')[:]
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) > 1:
                gemeinde = cols[1].get_text(strip=True)
                link_tag = cols[1].find('a', href=True)
                article_length = 0

                print(gemeinde)
                if link_tag:
                    gemeinde_url = 'https://de.wikipedia.org' + link_tag['href']
                    page.goto(gemeinde_url)
                    page.wait_for_load_state('networkidle')
                    gemeinde_content = page.content()
                    gemeinde_soup = BeautifulSoup(gemeinde_content, 'html.parser')
                    article_text = gemeinde_soup.find('div', {'class': 'mw-parser-output'}).get_text(strip=True)
                    article_length = len(article_text)

                data.append({'Gemeinde': gemeinde, 'Artikel_Laenge': article_length})

        browser.close()

        df = pd.DataFrame(data)
        df.to_csv('../data/scraped/wikipedia-length.csv', index=False)
        print(df.head())

scrape_gemeinden()
