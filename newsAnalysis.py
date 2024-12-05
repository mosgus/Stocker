import sys
import yfinance as yf
import time
from newsapi import NewsApiClient
from textblob import TextBlob
from openai import OpenAI

print("\nRunning newsAnalysis.py ↘️")
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
    return company_names


def make_names_list(symbols):
    """
    Creates a list of formatted names as "Name (Symbol)" for a list of stock symbols.
    """
    company_names = get_company_names(symbols)  # Fetch company names for the symbols
    nameList = [f"{name} ({symbol})" for symbol, name in company_names.items()]  # Create a list of formatted names
    print(f"Company Names: {nameList}")  # Print the list of company names
    return nameList


def get_stock_news(newsapi_key, stock, max_articles):
    """
    Fetches up to `max_articles` news article titles and URLs for the specified stock symbol.
    """
    try:
        newsapi = NewsApiClient(api_key=newsapi_key)
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


def analyze_sentiment(title):
    """
    Analyzes the sentiment of a news title and returns a score:
    -1 for negative sentiment, 0 for neutral, and 1 for positive sentiment.
    """
    sentiment = TextBlob(title).sentiment.polarity
    if sentiment > 0.1:
        return 1  # Positive sentiment
    elif sentiment < -0.1:
        return -1  # Negative sentiment
    else:
        return 0  # Neutral sentiment


def gpt_analysis(gpt_key, stock, articles):
    """
    Uses GPT API to summarize articles and provide a sentiment score for the stock.
    """
    client = OpenAI(api_key=gpt_key)
    try:

        #titles = "\n".join([f"{i + 1}. {article['title']}" for i, article in enumerate(articles)])
        prompt = (
            f"You are an expert financial analyst. Analyze the following news articles about {stock}. "
            "Provide a single paragraph summarizing the overall sentiment and context of the articles. "
            "Focus on key themes and trends rather than individual article summaries. "
            "Based on your analysis, assign a sentiment score ranging from -5 (very negative) to 5 (very positive), 0 being neutal "
            "that reflects the collective sentiment on this stock's growth potential. Don't be conservative with negative sentiment."
            "State this sentiment score on a new line and as the last output of your response."
            "(ex: GPT Sentiment Score: -2\n"
            f"{articles}"
        )

        # Query GPT API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        if response and response.choices:
            gpt_response = response.choices[0].message.content
            return gpt_response
        else:
            return "Error: GPT did not return a response."
    except Exception as e:
        return f"Error querying GPT: {e}"


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
        print(f"\nTop articles related to {entry}:")

        # Get news articles
        articles = get_stock_news(newsapi_key, entry, max_articles=5)

        total_score = 0  # Initialize total score as 0
        # Print the articles with sentiment scores
        for i, article in enumerate(articles, start=1):
            time.sleep(0.2)
            title = article['title']
            score = analyze_sentiment(title)
            total_score += score  # Accumulate the sentiment score
            print(f"  {i}. {title} - {article['url']} - [Sentiment Score: {score}]")

        # Print the total sentiment score for all articles
        print(f"TextBlob Sentiment Score for {entry}: {total_score}")

        # Use GPT for a generalized analysis
        print("\nGPT Analysis:")
        gpt_response = gpt_analysis(gpt_key, entry, articles)
        print(gpt_response)
        print(f"Done with News Sentiment Analysis for {entry}.✅")
        time.sleep(0.5)