# Stocker 📉👁️📈
A stock portfolio evaluater software developed by me (Gunnar B)

### Dependencies
To run properly you must provide api keys for chatGPT and NewsAPI
```bash
pip install openai
pip install newsapi-python
pip install yfinance --upgrade --no-cache-dir 
```
- yfinance seeks to limit queries with every update, making older versions redundant. 
- Using the pip install above removes redundant versions and installs working ones.
- I may migrate from yfinance to another alternative like Alpha Vantage, Tiingo, or Bloomberg.
- Be aware, using 'openai migrate' may cause issues depending on your OS. 
It's recommended to use ' grit apply openai ' for migrating the code effectively.


### How to Run
Either simply run setup.py and provide api keys when prompted or run setup.py with the keys as command-line arguments.
- Example:
  ```bash
  python setup.py
  ```
  OR
  ```bash
  python setup.py <chatGPT API key> <NewsAPI key>
  ```

