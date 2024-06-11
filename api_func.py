import requests
import numpy as np
import pandas as pd
import yfinance as yf
from config import api_key
from textblob import TextBlob
from datetime import timedelta
from sqlalchemy import create_engine

def get_avg_sentiment_scores(tickers):
    textual_data = {}

    for ticker in tickers:
        headlines = fetch_news(api_key, ticker)
        textual_data[ticker] = headlines

    # Analyzing sentiment for each headline and averaging the scores
    average_sentiment_scores = {}

    for ticker, headlines in textual_data.items():
        sentiments = [TextBlob(headline).sentiment.polarity if headline else 0 for headline in headlines]
        average_sentiment_scores[ticker] = np.mean(sentiments)

    # Extract tickers and sentiment scores
    tickers = list(average_sentiment_scores.keys())
    sentiment_scores = list(average_sentiment_scores.values())

    df = pd.DataFrame({"Ticker": tickers, "Sentiment Score":sentiment_scores})
    load_data_to_db(df, "Average_Sentiment_Score")

def fetch_all_stock_data(tickers, start='2023-04-01', end='2024-04-01'):
    engine = create_engine('sqlite:///stock_market_analysis.sqlite')

    stock_data = {ticker: yf.download(ticker, start, end) for ticker in tickers}
    
    print('Stock Data: ',stock_data)

    for ticker, df in stock_data.items():
        df['Ticker'] = ticker

    combined_df = pd.concat(stock_data.values())

    print('Data to stock_history: ',combined_df)

    combined_df.to_sql('stock_history', con=engine, if_exists='replace', index=True)
    
    get_avg_sentiment_scores(tickers)

    return '<h1>SQLite Database was updated</h1>'

# Function to fetch headlines from NewsAPI
def fetch_news(api_key, ticker):
    base_url = "https://newsapi.org/v2/everything"
    params = {
        'q': ticker,             # Search query (ticker symbol)
        'sortBy': 'publishedAt', # Sort by publication date
        'apiKey': api_key        # Your NewsAPI key
    }
    response = requests.get(base_url, params=params)
    articles = response.json().get('articles', [])
    headlines = [article['title'] for article in articles]
    return headlines

def load_data_to_db(data, ticker):
    """
    Loads transformed data into the SQLite database.
    """
    engine = create_engine('sqlite:///stock_market_analysis.sqlite')
    data.to_sql(ticker, con=engine, if_exists='replace', index=True)

def read_data(ticker):
    """
    Reads the data for the specified ticker from the SQLite database.
    """
    engine = create_engine('sqlite:///stock_market_analysis.sqlite')
    query = f"SELECT * FROM '{ticker}'"
    data = pd.read_sql_query(query, con=engine)
    return data

def calculate_daily_return(stock_data):
    """
    Calculates the daily return from the closing prices.
    """
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    return stock_data

def plot_moving_averages(stock_data, ticker):
    data = stock_data[ticker]
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['SMA_50'], label='50-Day SMA')
    plt.plot(data['SMA_200'], label='200-Day SMA')
    plt.title(f"{ticker} - Moving Averages")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.show()

def predict_monthly_prices(model, last_known_price, last_known_date, months=36):
    future_prices = []
    future_dates = []
    current_price = last_known_price
    
    for month in range(months):
        # Approximating each month by 21 trading days
        for day in range(21):
            next_input = pd.DataFrame(data=[[current_price]], columns=['Previous Close'])
            current_price = model.predict(next_input)[0]
        
        future_prices.append(current_price)
        # Assuming last_known_date is a datetime object; add roughly 30 days for each month
        last_known_date += timedelta(days=30)
        future_dates.append(last_known_date)
    
    return future_dates, future_prices

# Objective Function (Negative Sharpe Ratio)
def neg_sharpe_ratio(weights, expected_returns, cov_matrix, risk_free_rate=0.01):
    p_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    p_ret = np.dot(weights, expected_returns)
    return -(p_ret - risk_free_rate) / np.sqrt(p_var)

def analyze_sentiment(text):
    """Analyze the sentiment of a text and return polarity and subjectivity."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def main():
    tickers = ['MSFT', 'CRM', 'CRWD', 'ZM', 'SHOP', 'AAPL']

    for ticker in tickers:
        print(f"Fetching news for: {ticker}")
        articles = fetch_news(api_key, ticker)
        if articles['status'] == 'ok':
            for article in articles['articles'][:5]:  # Show only the first 5 articles for brevity
                description = article.get('description') or article.get('title')
                polarity, subjectivity = analyze_sentiment(description)
                print(f"Ticker: {ticker}, Title: {article['title']}")
                print(f"Sentiment Polarity: {polarity:.2f}, Sentiment Subjectivity: {subjectivity:.2f}")
                print(f"URL: {article['url']}\n")
    
    return articles

def fetch_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="5y")
    return data['Close']

def calculate_parameters(tickers):
    prices = {ticker: fetch_data(ticker) for ticker in tickers}
    prices = pd.DataFrame(prices)
    daily_returns = prices.pct_change()
    annual_mean_returns = daily_returns.mean() * 252
    annual_std_devs = daily_returns.std() * np.sqrt(252)
    return {ticker: {'mean': annual_mean_returns[ticker], 'std': annual_std_devs[ticker]}
            for ticker in tickers}

def calculate_expected_returns(tickers):
    prices = pd.DataFrame({ticker: fetch_data(ticker) for ticker in tickers})
    daily_returns = prices.pct_change()
    average_daily_returns = daily_returns.mean()
    annual_expected_returns = average_daily_returns * 252  # Convert to annual returns
    return annual_expected_returns