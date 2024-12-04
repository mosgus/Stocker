import os
import sys
import glob
import pandas as pd
import subprocess
import time

print("Running Stocker.py ↘️")
time.sleep(0.5)

def get_symbols_from_user():
    """
    Prompt user for symbols
    """
    symbols_input = input("Enter stock symbols (comma-separated), or press Enter to scan CSV files: ").strip()
    if symbols_input:
        # Split input into a list, remove whitespace, and make uppercase
        symbols = [symbol.strip().upper() for symbol in symbols_input.split(",")]
        return symbols
    return None

def get_symbols_from_csv(directory="symbol_lists"):
    """
    Collect all stock symbols from CSV files in the specified directory.
    Supports files with or without headers.
    Ignores duplicates.
    """
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in directory '{directory}'.")
        return []

    all_symbols = set()
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, header=None)
            all_symbols.update(df.stack().str.upper().dropna().unique())
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")

    return list(all_symbols)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: API key not provided. Exiting...")
        sys.exit(1)

    gpt_key = sys.argv[1]  # Retrieve the API keys passed from setup.py
    newsapi_key = sys.argv[2]
    print(f"GPT API key received: {gpt_key[:16]}...")
    print(f"NewsAPI API Key: {newsapi_key[:16]}... ")

    # Get symbols from user input or CSV files
    symbols = get_symbols_from_user()
    if not symbols:
        symbols = get_symbols_from_csv()

    # Print the final list of symbols
    time.sleep(0.5)
    symbols = list(set(symbol.strip() for symbol in symbols))
    print(f"Portfolio w/out dupes: {symbols}")
    time.sleep(0.5)
    print("Passing data to newsGetter.py...📰")
    time.sleep(1)
    subprocess.run(["python", "newsGetter.py", gpt_key, newsapi_key, *symbols])