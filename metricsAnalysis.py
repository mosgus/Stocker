from openai import OpenAI
import sys
import yfinance as yf
import pandas as pd
import time
import os

print("\nRunning metricsAnalysis.py ↘️")
time.sleep(0.5)

def gpt_risk_analysis(symbol, beta, sharpe_ratio, volatility, gpt_key):
    """
    Analyzes the stock's risk metrics using GPT API and provides a risk assessment score and analysis.
    """
    client = OpenAI(api_key=gpt_key)
    try:
        prompt = (
            f"You are an expert financial analyst. Analyze the following risk metrics for the stock '{symbol}':\n"
            f"- Beta: {beta}\n"
            f"- Volatility: {volatility}\n"
            f"- Sharpe Ratio: {sharpe_ratio}\n"
            "Provide a short paragraph discussing the implications of these metrics. Discuss the stock's risk and return profile based on these metrics. "
            "Finally, assign a 'risk score' between 1 (very low risk) and 5 (very high risk). "
            "State this risk score on a new line and as the last output of your response."
            "(ex: GPT Risk Score for NETGEAR, Inc.(NTGR): 2"
        )

        # Query GPT API
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": prompt}]
        )

        if response and response.choices:
            gpt_response = response.choices[0].message.content
            return gpt_response
        else:
            return "Error: GPT did not return a response."
    except Exception as e:
        return f"Error querying GPT: {e}"

def parse_gpt_response(gpt_response):
    """
    Parses GPT response to extract the analysis and risk score separately.
    """
    try:
        # Extract Risk Score
        risk_score = None
        for line in reversed(gpt_response.splitlines()):
            if "Risk Score" in line:  # Expected format: "Risk Score: <value>"
                risk_score = int(line.split(":")[-1].strip())
                break

        # Remove "Risk Score" line from the analysis
        cleaned_analysis = "\n".join(
            line for line in gpt_response.splitlines() if "Risk Score" not in line
        ).strip()

        return cleaned_analysis, risk_score
    except ValueError:
        print("Error parsing GPT response. Returning None for risk score and cleaned analysis.")
        return gpt_response, None

def calculate_metrics(symbol, market_data, rf_rate, gpt_key):
    """
    Calculates metrics such as Beta, Sharpe Ratio, and Volatility for a given stock.
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

        # Calculate Beta (Covariance / Variance)
        covariance = combined['Stock Return'].cov(combined['Market Return'])
        variance = combined['Market Return'].var()
        beta = covariance / variance

        # Calculate Sharpe Ratio (Excess return / Standard deviation)
        avg_stock_return = combined['Stock Return'].mean() * 252  # Annualized return
        std_dev = combined['Stock Return'].std() * (252 ** 0.5)  # Annualized volatility
        sharpe_ratio = (avg_stock_return - rf_rate) / std_dev

        # Get GPT Risk Analysis
        gpt_response = gpt_risk_analysis(symbol, round(beta, 4), round(sharpe_ratio, 4), round(std_dev, 4), gpt_key)
        cleaned_analysis, risk_score = parse_gpt_response(gpt_response)

        # Return a dictionary of metrics
        return {
            "Symbol": symbol,
            "Beta": round(beta, 4),
            "Volatility": round(std_dev, 4),
            "Sharpe Ratio": round(sharpe_ratio, 4),
            "GPT Risk Score": risk_score,
            "GPT Analysis": cleaned_analysis
        }

    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return {
            "Symbol": symbol, "Beta": None, "Volatility": None, "Sharpe Ratio": None, "GPT Risk Score": None, "GPT Analysis": None
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
        metrics = calculate_metrics(symbol, sp500_data, rf_rate, gpt_key)

        # Display shortened GPT Analysis in console
        print(f"Metrics for {symbol}: {metrics}")

        metrics_list.append(metrics)

    # Save metrics to CSV
    os.makedirs("analysis", exist_ok=True)
    output_file = "analysis/metricsAnalysis.csv"
    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv(output_file, index=False)
    print(f"\nMetrics analysis saved to {output_file}")