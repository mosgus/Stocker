import sys
import yfinance as yf
import time
from newsapi import NewsApiClient

print("\nRunning newsGetter.py ↘️")
time.sleep(0.5)

def get_company_names(symbols):
    """
    Retrieves company names for the list of symbols.
    """
    company_names = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            company_names[symbol] = ticker.info.get('shortName', 'Unknown Company')
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            company_names[symbol] = 'Unknown Company'
    return company_names


def make_names_list(symbols):
    """
    Creates a list of formatted names as "Name (Symbol)" for a list of stock symbols.
    """
    company_names = get_company_names(symbols)  # Fetch company names for the symbols
    nameList = [f"{name} ({symbol})" for symbol, name in company_names.items()]  # Create a list of formatted names
    print(f"Company Names: {nameList}")  # Print the list of company names
    return nameList


def get_stock_news(newsapi_key, stock, max_articles=5):
    """
    Fetches up to `max_articles` news article titles and URLs for the specified stock symbol.
    """
    try:
        # Initialize the NewsAPI client
        newsapi = NewsApiClient(api_key=newsapi_key)

        # Construct the query string
        query = f"{stock}"

        # Fetch news articles for the stock symbol
        all_articles = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=max_articles,
        )

        # Extract and return article titles and URLs
        articles = [
            {"title": article['title'], "url": article['url']}
            for article in all_articles.get('articles', [])
        ]
        return articles
    except Exception as e:
        print(f"Error fetching news for {stock}: {e}")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Error: Insufficient arguments provided. Exiting...")
        sys.exit(1)

    # Extract API keys and symbols passed as command-line arguments
    gpt_key = sys.argv[1]
    newsapi_key = sys.argv[2]
    symbols = sys.argv[3:]
    print(f"Received Symbols: {symbols}")

    # Generate a list of company names with symbols
    nameList = make_names_list(symbols)

    # Fetch news for each company in the name list
    print("Fetching news articles for each company...")
    time.sleep(1)
    for entry in nameList:
        # Use the full "Name (Symbol)" format for the query
        print(f"    Top articles related to {entry}:")

        # Get news articles
        articles = get_stock_news(newsapi_key, entry, max_articles=5)

        # Print the articles
        for i, article in enumerate(articles, start=1):
            time.sleep(0.2)
            print(f"      {i}. {article['title']} - {article['url']}")

        time.sleep(0.5)