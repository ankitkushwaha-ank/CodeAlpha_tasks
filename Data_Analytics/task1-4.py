import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# =====================
# TASK 2: SCRAPING DATA
# =====================
def scrape_amazon(search_query, pages=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }

    base_url = "https://www.amazon.in/s"
    products = []

    for page in range(1, pages + 1):
        params = {"k": search_query, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select(".s-result-item"):
            # Product Name
            name = item.select_one("h2 span")
            name = name.text.strip() if name else "N/A"

            # Price
            price = item.select_one(".a-price-whole")
            price = price.text.strip().replace(",", "") if price else "N/A"

            # Rating
            rating = item.select_one("span.a-icon-alt")
            rating = rating.text.strip() if rating else "N/A"

            # Link
            link = item.select_one("a.a-link-normal")
            link = "https://www.amazon.in" + link["href"] if link else "N/A"

            products.append({
                "Product Name": name,
                "Price": price,
                "Rating": rating,
                "Link": link
            })

    return products


# =====================
# TASK 3: SAVE TO CSV
# =====================
def save_to_csv(products, filename="amazon_products.csv"):
    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✅ Data saved to {filename}")
    return df


# =====================
# TASK 4: ANALYSIS + VISUALIZATION
# =====================
def analyze_data(df):
    # Convert price to numeric
    df["Price"] = pd.to_numeric(df["Price"].str.replace(",", ""), errors="coerce")

    # Extract numeric rating (first number before "out of 5")
    df["Rating"] = df["Rating"].str.extract(r"([0-9.]+)").astype(float)

    print("\n📊 Dataset Summary:")
    print(df.describe(include="all"))

    # Plot price distribution
    plt.figure(figsize=(8, 5))
    df["Price"].dropna().plot(kind="hist", bins=20, alpha=0.7)
    plt.title("Price Distribution of Amazon Products")
    plt.xlabel("Price (INR)")
    plt.ylabel("Frequency")
    plt.show()

    # Top 10 expensive products
    top10 = df.sort_values(by="Price", ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top10["Product Name"], top10["Price"])
    plt.title("Top 10 Expensive Products")
    plt.xlabel("Price (INR)")
    plt.show()


# =====================
# MAIN EXECUTION
# =====================
if __name__ == "__main__":
    query = "laptop"   # Change this to search anything
    data = scrape_amazon(query, pages=3)
    df = save_to_csv(data, "amazon_products.csv")
    analyze_data(df)
