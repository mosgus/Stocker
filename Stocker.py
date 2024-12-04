import os
import sys
import glob
import pandas as pd

print("Running Stocker.py ↘️")

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
    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return []

    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in directory '{directory}'.")
        return []

    all_symbols = set()
    for csv_file in csv_files:
        try:
            # Attempt to read the file as a CSV with headers
            try:
                df = pd.read_csv(csv_file)
                if 'Symbol' in df.columns:
                    # If a 'Symbol' column exists, use it
                    all_symbols.update(df['Symbol'].str.upper().dropna().unique())
                else:
                    raise ValueError("No 'Symbol' column found, treating as headerless file.")
            except ValueError:
                # Read the file as headerless and treat all data as symbols
                df = pd.read_csv(csv_file, header=None)
                all_symbols.update(df.stack().str.upper().dropna().unique())
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")

    return list(all_symbols)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: API key not provided. Exiting...")
        sys.exit(1)

    api_key = sys.argv[1]  # Retrieve the API key passed from setup.py
    print(f"API key received: {api_key[:16]}... (truncated for security)")

    # Get symbols from user input or CSV files
    symbols = get_symbols_from_user()
    if not symbols:
        symbols = get_symbols_from_csv()

    # Print the final list of symbols
    print("Consolidated list of stock symbols:")
    print(symbols) # TODO: remove dupes
    print("List w/ out duplicates:")
    symbols = list(set(symbol.strip() for symbol in symbols))
    print(symbols)