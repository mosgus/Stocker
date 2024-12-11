from openai import OpenAI
import sys
import yfinance as yf
import pandas as pd
import time
import os

print("\nRunning metricsAnalysis.py ↘️")
time.sleep(0.5)

def calculate_metrics(symbol, market_data, rf_rate, market_return):
    """
    Calculates metrics such as CAPM Expected Return and Sharpe Ratio for a given stock.
    Can be extended to calculate additional metrics.
    """
    try:
        # Fetch historical data for the stock
        stock = yf.Ticker(symbol)
        stock_data = stock.history(period="5y")  # 5 years of historical data
        stock_data['Daily Return'] = stock_data['Close'].pct_change()

        # Merge stock returns with market returns
        combined = pd.DataFrame({
            'Stock Return': stock_data['Daily Return'],
            'Market Return': market_data['Daily Return']
        }).dropna()
        ''' RISK '''

        # Calculate Beta (Covariance / Variance)
        covariance = combined['Stock Return'].cov(combined['Market Return'])
        variance = combined['Market Return'].var()
        beta = covariance / variance # Beta tells you about the stock’s exposure to market movements.
        # CAPM Expected Return
        capm_expected_return = rf_rate + beta * (market_return - rf_rate)
        # Sharpe Ratio (Excess return / Standard deviation)
        avg_stock_return = combined['Stock Return'].mean() * 252  # Annualized return
        std_dev = combined['Stock Return'].std() * (252 ** 0.5)  # Annualized volatility
        sharpe_ratio = (avg_stock_return - rf_rate) / std_dev
        ''' RISK '''

        # Return a dictionary of metrics
        return {
            "Symbol": symbol,
            "Beta": round(beta, 4),
            "CAPM Expected Return": round(capm_expected_return, 4),
            "Sharpe Ratio": round(sharpe_ratio, 4)
        }

    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return {
            "Symbol": symbol, "Beta": None, "CAPM Expected Return": None,"Sharpe Ratio": None
        }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Insufficient arguments provided. Exiting...")
        sys.exit(1)

    # Extract API key and symbols passed as command-line arguments
    gpt_key = sys.argv[1]
    symbols = sys.argv[2:]
    print(f"Received Symbols: {symbols}")

    # Fetch 10-Year Treasury Yield (^TNX) & Calculate historical market return (S&P 500)
    risk_free = yf.Ticker("^TNX")
    rf_rate = risk_free.history(period="1d")['Close'].iloc[-1] / 100  # Convert to percentage
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(period="5y")
    sp500_data['Daily Return'] = sp500_data['Close'].pct_change()
    market_return = sp500_data['Daily Return'].mean() * 252  # Annualized return
    print(f"📊Market Return: {market_return:.4f} & Risk-Free Rate: {rf_rate:.4f}")

    # Analyze metrics for each symbol
    metrics_list = []
    for symbol in symbols:
        print(f"\nAnalyzing metrics for {symbol}...")
        metrics = calculate_metrics(symbol, sp500_data, rf_rate, market_return)
        metrics_list.append(metrics)
        print(f"Metrics for {symbol}: {metrics}")

    # Save metrics to CSV
    os.makedirs("analysis", exist_ok=True)
    output_file = "analysis/metricsAnalysis.csv"
    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv(output_file, index=False)
    print(f"\nMetrics analysis saved to {output_file}")