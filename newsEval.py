import sys
import yfinance as yf
import time

print("\nRunning newsEval.py ↘️")
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
    Processes symbols using the provided API keys and fetches company names.
    """
    # Fetch company names for the symbols
    company_names = get_company_names(symbols)

    # Create a list of formatted names as "Name (Symbol)"
    nameList = [f"{name}({symbol})" for symbol, name in company_names.items()]

    # Print the formatted list of company names
    print(f"Company Names: {nameList}")

    # Return the name list if needed for further processing
    return nameList


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Error: Insufficient arguments provided. Exiting...")
        sys.exit(1)

    # Extract the API keys and symbols from arguments
    gpt_key = sys.argv[1]
    newsapi_key = sys.argv[2]
    symbols = sys.argv[3:]
    print(f"Received Symbols: {symbols}")

    # Using the list of symbols, get the associated company names to make NewsAPI queries easy
    nameList = make_names_list(symbols)