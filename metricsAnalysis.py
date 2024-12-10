import sys
import yfinance as yf
import time
from openai import OpenAI
import csv
import os

print("\nRunning metricsAnalysis.py ↘️")
time.sleep(0.5)

if __name__ == "__main__":
    # Extract API keys and symbols
    gpt_key = sys.argv[1]
    symbols = sys.argv[2:]
    print(f"Received GPT API Key: {gpt_key[:16]}...")
    print(f"Received Symbols: {symbols}")

    # Placeholder for metrics analysis
    print("Placeholder: Metrics analysis will be implemented here in the future.")