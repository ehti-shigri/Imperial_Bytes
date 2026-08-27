import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Rating map conversion dictionary
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_multi_page_products(num_pages=5):
    """
    Scrapes product data across multiple pages from Books to Scrape.
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    scraped_products = []

    print("=" * 60)
    print(f"       STARTING WEB SCRAPING ({num_pages} PAGES)       ")
    print("=" * 60)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for page in range(1, num_pages + 1):
        url = base_url.format(page)
        print(f"Fetching Page {page}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f" -> Failed to retrieve page {page} (Status Code: {response.status_code})")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("article", class_="product_pod")

            for item in products:
                # Extract Title
                title_tag = item.find("h3").find("a")
                title = title_tag.get("title", title_tag.text.strip())

                # Extract Price
                price_text = item.find("p", class_="price_color").text.strip()
                cleaned_price_str = "".join([char for char in price_text if char.isdigit() or char == '.'])
                price = float(cleaned_price_str) if cleaned_price_str else np.nan

                # Extract Rating
                rating_tag = item.find("p", class_="star-rating")
                rating_class = rating_tag.get("class", []) if rating_tag else []
                rating_str = [c for c in rating_class if c != "star-rating"]
                rating_num = RATING_MAP.get(rating_str[0], np.nan) if rating_str else np.nan

                # Extract Availability Status
                availability_tag = item.find("p", class_="instock availability")
                availability = availability_tag.text.strip() if availability_tag else "Unknown"

                scraped_products.append({
                    "title": title,
                    "price_gbp": price,
                    "rating": rating_num,
                    "availability": availability
                })

            time.sleep(0.3)

        except Exception as e:
            print(f"Error scraping page {page}: {e}")

    df = pd.DataFrame(scraped_products)
    print(f"\n[SCRAPING COMPLETED] Total products collected: {len(df)}")
    return df

def clean_and_analyze_products(df):
    """
    Cleans scraped data, performs statistical analysis, handles missing values,
    and stores in CSV.
    """
    print("\n" + "=" * 60)
    print("        PRODUCT DATA ANALYSIS REPORT        ")
    print("=" * 60)

    # 1. Dataset Overview
    print("\n--- Scraped Dataset Overview ---")
    print(f"Total Products: {df.shape[0]}")
    print(f"Total Attributes: {df.shape[1]}")
    print("\nFirst 5 Scraped Rows:")
    print(df.head())

    # 2. Look for Missing Values
    print("\n" + "=" * 60)
    print("[1] LOOKING FOR MISSING VALUES")
    print("=" * 60)
    missing_vals = df.isnull().sum()
    print("Missing values count per column:")
    print(missing_vals)

    # 3. Fill Missing Values (Data Cleaning & Imputation)
    print("\n" + "=" * 60)
    print("[2] FILLING MISSING VALUES (IMPUTATION STRATEGY)")
    print("=" * 60)
    
    if df["price_gbp"].isnull().sum() > 0:
        median_price = df["price_gbp"].median()
        df["price_gbp"] = df["price_gbp"].fillna(median_price)
        print(f"Filled missing price_gbp with median: GBP {median_price:.2f}")

    if df["rating"].isnull().sum() > 0:
        mode_rating = df["rating"].mode()[0]
        df["rating"] = df["rating"].fillna(mode_rating)
        print(f"Filled missing rating with mode: {mode_rating}")

    df["availability"] = df["availability"].fillna("Unknown")

    print("Missing values after filling:")
    print(df.isnull().sum())

    # Save cleaned data to CSV
    csv_filename = "products_scraped.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\n -> Saved raw & cleaned products dataset to '{csv_filename}'")

    # 4. Highest Price Product
    print("\n" + "=" * 60)
    print("[3] HIGHEST PRICED PRODUCT")
    print("=" * 60)
    max_price = df["price_gbp"].max()
    highest_priced = df[df["price_gbp"] == max_price]
    print(f"Highest Product Price: GBP {max_price:.2f}")
    print("\nProduct(s) with Highest Price:")
    print(highest_priced[['title', 'price_gbp', 'rating', 'availability']].to_string(index=False))

    # 5. Lowest Price Product
    print("\n" + "=" * 60)
    print("[4] LOWEST PRICED PRODUCT")
    print("=" * 60)
    min_price = df["price_gbp"].min()
    lowest_priced = df[df["price_gbp"] == min_price]
    print(f"Lowest Product Price: GBP {min_price:.2f}")
    print("\nProduct(s) with Lowest Price:")
    print(lowest_priced[['title', 'price_gbp', 'rating', 'availability']].to_string(index=False))

    # 6. Average Price Analysis
    print("\n" + "=" * 60)
    print("[5] AVERAGE PRODUCT PRICE ANALYSIS")
    print("=" * 60)
    avg_price = df["price_gbp"].mean()
    median_price = df["price_gbp"].median()
    print(f"Mean (Average) Product Price: GBP {avg_price:.2f}")
    print(f"Median Product Price:       GBP {median_price:.2f}")

    # 7. Rating-wise Price Analysis
    print("\n" + "=" * 60)
    print("[6] RATING-WISE PRICE & COUNT ANALYSIS")
    print("=" * 60)
    rating_summary = df.groupby("rating")["price_gbp"].agg(
        Average_Price='mean',
        Min_Price='min',
        Max_Price='max',
        Product_Count='count'
    ).reset_index().sort_values(by="rating", ascending=False)

    print(rating_summary.to_string(index=False))

    # 8. Top Performers (Top Rated Products: Rating 5 Stars)
    print("\n" + "=" * 60)
    print("[7] TOP PERFORMERS (5-STAR RATED PRODUCTS)")
    print("=" * 60)
    top_performers = df[df["rating"] == 5]
    pct_top = (len(top_performers) / len(df)) * 100
    print(f"Total 5-Star Rated Products: {len(top_performers)} out of {len(df)} ({pct_top:.1f}%)")
    print("\nSample Top Performers:")
    print(top_performers[['title', 'price_gbp', 'rating', 'availability']].head(10).to_string(index=False))

    # 9. Price Distribution Summary Stats
    print("\n" + "=" * 60)
    print("[8] PRICE DISTRIBUTION SUMMARY")
    print("=" * 60)
    print(df["price_gbp"].describe().to_string())

    print("\n[SUCCESS] Product Web Scraper & Analysis Completed Successfully!\n")

if __name__ == "__main__":
    raw_df = scrape_multi_page_products(num_pages=5)
    clean_and_analyze_products(raw_df)
