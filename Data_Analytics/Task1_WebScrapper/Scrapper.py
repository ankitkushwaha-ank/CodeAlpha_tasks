import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time


# Function to get HTML content with headers (avoid bot detection)
def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "en-IN,en;q=0.9"
    }
    response = requests.get(url, headers=headers)
    return response.text


# Function to scrape Amazon search results
def scrape_amazon(search_query, pages=1):
    base_url = "https://www.amazon.in/s?k="
    all_products = []

    for page in range(1, pages + 1):
        url = f"{base_url}{search_query}&page={page}"
        print(f"Scraping page {page}: {url}")

        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")

        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in products:
            # ---- Product Name ----
            name = "N/A"
            try:
                title_tag = item.h2.find("span")
                if title_tag:
                    name = title_tag.get_text(strip=True)
            except:
                pass

            # ---- Product Link ----
            link = "N/A"
            link_tag = item.find("a",
                                 class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
            if not link_tag:
                link_tag = item.find("a", class_="a-link-normal s-no-outline")  # fallback for some products

            if link_tag and "href" in link_tag.attrs:
                raw_link = link_tag["href"]
                if "/dp/" in raw_link:  # clean link format
                    link = "https://www.amazon.in" + raw_link.split("?")[0]
                else:
                    link = "https://www.amazon.in" + raw_link

            # ---- Price ----
            try:
                price = item.find("span", class_="a-price-whole").get_text(strip=True)
            except:
                price = "N/A"

            # ---- Rating ----
            try:
                rating = item.find("span", class_="a-icon-alt").get_text(strip=True)
            except:
                rating = "N/A"

            # ---- Save Data ----
            all_products.append({
                "Product Name": name,
                "Price": price,
                "Rating": rating,
                "Link": link
            })

        # Sleep to avoid blocking
        time.sleep(random.randint(2, 5))

    return all_products


# Run scraper
data = scrape_amazon("laptop", pages=2)  # Scrape 2 pages of laptops

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("amazon_products.csv", index=False, encoding="utf-8")
print("✅ Data saved to amazon_products.csv")
