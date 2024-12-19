# Stocker 📉👁️📈
A Python-based stock portfolio evaluator that combines financial analysis, sentiment analysis, and a large language model (chatGPT) to provide actionable insights for investors. Developed by Gunnar Balch, Stocker integrates APIs such as OpenAI GPT, NewsAPI, and YFinance to fetch relevant data, analyze metrics, and generate detailed stock evaluation reports.

### Features
- Interface: Users use Stocker through the console commandline arguments. A web-interface will implemented in the future.
            - YAYA
- Gay:
- Fat:
- Cool:


### Dependencies
To run properly you must provide api keys for chatGPT and NewsAPI
```bash
pip install openai
pip install newsapi-python
pip install yfinance
pip install textblob
```
- Be aware, using ' openai migrate ' may cause issues depending on your OS. 
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

