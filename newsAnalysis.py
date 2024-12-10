import sys
import yfinance as yf
import time
from newsapi import NewsApiClient
from textblob import TextBlob
from openai import OpenAI
import csv
import os

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
    nameList = [f"{name}({symbol})" for symbol, name in company_names.items()]  # Create a list of formatted names
    #nameList = [f"{name}" for symbol, name in company_names.items()] # without the symbol( for query testing )
    print(f"Company Names: {nameList}")  # Print the list of company names
    return nameList


def get_stock_news(newsapi_key, stock):
    """
    Fetches news article titles and URLs for the specified stock symbol.
    """
    try:
        newsapi = NewsApiClient(api_key=newsapi_key)
        query = f"{stock}"
        # Fetch news articles for the stock symbol
        all_articles = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size= 5,
        )

        # Extract and return article titles and URLs
        articles = [
            {
                "title": article['title'],
                "description": article.get('description', 'No description available.'),
                "url": article['url']}
            for article in all_articles.get('articles', [])
        ]
        return articles
    except Exception as e:
        print(f"Error fetching news for {stock}: {e}")
        return []


def tb_sentiment(title):
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
        prompt = (
            f"You are an expert financial analyst. Analyze the following news articles about {stock}. "
            "Provide a single paragraph summarizing the overall sentiment and context of the articles. "
            "Focus on key themes and trends rather than individual article summaries. "
            "Based on your analysis, assign a sentiment score ranging from -5 (very negative) to 5 (very positive), 0 (neutral) "
            "that reflects the collective sentiment on this stock's growth potential. Don't be conservative with negative sentiment."
            "State this sentiment score on a new line and as the last output of your response."
            "(ex: GPT Sentiment Score for NETGEAR, Inc.(NTGR): -2\n"
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

def extract_gpt_score(response):
    """
    Extracts the sentiment score from GPT's response.
    """
    try:
        lines = response.splitlines()
        for line in reversed(lines):
            if "GPT Sentiment Score" in line:
                score = line.split(":")[-1].strip()
                return int(score)
    except ValueError:
        print("Error parsing GPT sentiment score.")
    return None

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
    score_file = os.path.join("scores", "newsScores.csv")
    analysis_file = os.path.join("GPTanalysis", "newsAnal.csv")

    # Prepare the CSV file
    # Prepare the scores CSV file
    with open(score_file, mode="w", newline="", encoding="utf-8") as scores_csv, \
            open(analysis_file, mode="w", newline="", encoding="utf-8") as analysis_csv:

        score_writer = csv.writer(scores_csv)
        analysis_writer = csv.writer(analysis_csv)

        # Write headers to both CSV files
        score_writer.writerow(["Stock", "TextBlob Score", "GPT Score"])
        analysis_writer.writerow(["Stock", "Analysis"])

        # Fetch news for each company in the name list
        print("Fetching news articles for each company and analyzing sentiment...")
        time.sleep(1)

        for entry in nameList:
            print(f"\nTop articles related to {entry}:")
            symbol = entry.split("(")[-1].strip(")")  # Extract the stock symbol

            # Fetch news articles
            articles = get_stock_news(newsapi_key, entry)

            # Calculate TextBlob total sentiment score
            tbTotal_score = 0
            for i, article in enumerate(articles, start=1):
                time.sleep(0.2)
                tb_score = tb_sentiment(article['title'])
                tbTotal_score += tb_score  # Accumulate TextBlob sentiment score
                print(f"  {i}. {article['title']} "
                      f"\n      ℹ - {article['description']}"
                      f"\n      {article['url']} "
                      f"\n      [Sentiment Score: {tb_score}]")

            print(f"\nTextBlob Sentiment Score for {entry}: {tbTotal_score}")

            # GPT Analysis
            print("\nGPT Analysis:")
            gpt_response = gpt_analysis(gpt_key, entry, articles)
            print(gpt_response)

            # Extract GPT Sentiment Score
            gpt_score = None
            gpt_analysis_text = gpt_response
            try:
                for line in reversed(gpt_response.splitlines()):
                    if "GPT Sentiment Score" in line:
                        gpt_score = int(line.split(":")[-1].strip()) # Extract info proceeding "Sentiment Score:"
                        gpt_analysis_text = gpt_response.replace(line, "").strip() # Remove the sentiment score from the analysis text
                        break
            except ValueError:
                print(f"Error parsing GPT sentiment score for {entry}.")
                gpt_score = None

            # Write to the scores CSV
            score_writer.writerow([symbol, tbTotal_score, gpt_score])

            # Write to the analysis CSV
            analysis_writer.writerow([symbol, gpt_analysis_text])

            print(f"\nDone with News Sentiment Analysis for {entry}✅")
            time.sleep(0.5)

    print(f"Sentiment scores saved to {score_file}")
    print(f"GPT analysis saved to {analysis_file}")