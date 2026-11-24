import re
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def scrape_all_books(pages: int = 50) -> pd.DataFrame:
    records = []
    session = requests.Session()

    for page in range(1, pages + 1):
        url = f"{BASE_URL}catalogue/page-{page}.html"
        resp = session.get(url, timeout=15)
        resp.encoding = "utf-8"
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for book in articles:
            title = book.h3.a["title"]

            # Extract numeric price
            raw_price = book.find("p", class_="price_color").get_text(strip=True)
            price = float(re.sub(r"[^\d.]", "", raw_price))

            # Convert star rating class to integer
            rating_word = book.find("p", class_="star-rating")["class"][1]
            rating = RATING_MAP.get(rating_word, 0)

            # Resolve full image URL
            rel_img = book.find("img")["src"]
            image_url = urljoin(url, rel_img)

            # Resolve full book detail URL
            rel_link = book.h3.a["href"]
            book_url = urljoin(url, rel_link)

            records.append(
                {
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "image_url": image_url,
                    "book_url": book_url,
                }
            )

    df = pd.DataFrame(records)
    df.to_csv("books_data.csv", index=False)
    print(f"Scraped {len(df)} books successfully.")
    return df


if __name__ == "__main__":
    scrape_all_books()
