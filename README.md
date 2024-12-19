# Stocker 📉👁️📈
A Python-based stock portfolio evaluator that combines financial analysis, sentiment analysis, and a large language model (chatGPT) to provide actionable insights for investors. Developed by Gunnar Balch, Stocker integrates APIs such as OpenAI's chatGPT API, NewsAPI, and YFinance to fetch relevant data, analyze metrics, and generate detailed stock evaluation reports.

### Features
- **Interface**:
    - Users use Stocker through console commandline arguments. A web-interface will implemented in the future.
        - Users can store portfolio csv files in the /porfolios directory. Stocker will scan csv files in /porfolios if users DON'T provide a portfolio via commandline inputs.
- **Sentiment Analysis**:
    - NewsAPI aggregates recent and relevant articles pertaining to each stock's sentiment. A 'Sentiment Score' is assessed to each stock based on the overall sentiment expressed from all the articles. Both TextBlob and chatGPT are used to grade sentiment. Scores get saved as a csv file.
        - TextBlob's sentiment score is used as a baseline to compare with chatGPT's sentiment score.
        - ChatGPT analyzes a stock's articles as a whole, providing a paragraph synopsis explaining general sentiment, it then provides a sentiment score.
        - Sentiment Scores for both TextBlob and ChatGPT can range from -5(very negative sentiment) to +5(very positive sentiment).
- **Financial Metrics Analysis**:
          



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

