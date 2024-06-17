import os
import sqlite3
import sqlalchemy
import numpy as np
import pandas as pd
import yfinance as yf
from config import api_key
from textblob import TextBlob
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from flask import Flask, render_template, jsonify, request
from api_func import get_avg_sentiment_scores, read_data, load_data_to_db, fetch_news, fetch_all_stock_data

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/api/v1.0/load_data/<tickers>/<start>/<end>')
def load_data(tickers,start='2020-01-01',end='2024-01-01'):
    print(tickers,start,end)
    print('')
    fetch_all_stock_data(eval(tickers),start,end)
    return '<h1>Data has been loaded to the Database</h1>'

@app.route('/api/v1.0/stock_sentiment_score')
def get_sentiment():
    conn = sqlite3.connect('stock_market_analysis.sqlite')

    db = conn.cursor()

    df1 = pd.read_sql('SELECT * FROM Average_Sentiment_Score', conn)

    return df1.to_dict(orient='records')

@app.route('/api/v1.0/stock_history')
def get_data():

    conn = sqlite3.connect('stock_market_analysis.sqlite')

    db = conn.cursor()
    df = pd.read_sql('SELECT * FROM stock_history', conn)

    print('Data: ',df.columns)

    df.Date = df.Date.str.replace('\s.*','',regex=True)

    start_date = request.json.get('start_date')
    return df.to_dict(orient='records')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    tickers = data.get('tickers')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    results = {}
    if tickers and start_date and end_date:
        tickers_list = [ticker.strip() for ticker in tickers.split(',')]
        for ticker in tickers_list:
            try:
                stock_data = yf.download(ticker, start=start_date, end=end_date)
                if stock_data.empty:
                    results[ticker] = {'error': 'No data available for this ticker and date range'}
                else:
                    current_price = stock_data['Close'][-1]
                    predicted_price = predict_stock_price(stock_data)  # Example function
                    results[ticker] = {'current_price': current_price, 'predicted_price': predicted_price}
            except Exception as e:
                results[ticker] = {'error': str(e)}
    else:
        return jsonify({'error': 'Invalid input data'}), 400

    return jsonify(results)

def predict_stock_price(data):
    # Example prediction logic
    return data['Close'][-1] * 1.05  # Dummy prediction


    
# import os
# import pandas as pd
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine, text
# from flask import Flask, render_template, jsonify
# from api_func import fetch_all_stock_data

# app = Flask(__name__)

# # Set up SQLAlchemy database URI
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///stock_market_analysis.sqlite"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Set up SQLAlchemy engine and session
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# Session = sessionmaker(bind=engine)

# @app.route('/')
# def homepage():
#     return render_template('index.html')

#     return '<h1>Data has been loaded to the Database</h1>'

# @app.route('/api/v1.0/stock_sentiment_score')
# def get_sentiment():
#     session = Session()
#     try:
#         result = session.execute(text('SELECT * FROM Average_Sentiment_Score')).fetchall()
#         if result:
#             df1 = pd.DataFrame(result, columns=result[0].keys())
#             print('Sentiment Data:', df1.to_dict(orient='records'))  # Log the data to inspect
#             return df1.to_json(orient='records')
#         else:
#             return jsonify([])  # Return an empty list if no results
#     except Exception as e:
#         logging.error(f"Error fetching sentiment scores: {e}")
#         return jsonify(error=str(e)), 500
#     finally:
#         session.close()


# @app.route('/api/v1.0/stock_history')
# def get_data():
#     session = Session()
#     try:
#         result = session.execute(text('SELECT * FROM stock_history')).fetchall()
#         if result:
#             df2 = pd.DataFrame(result, columns=result[0].keys())
#             df2['Date'] = df2['Date'].str.replace(r'\s.*', '', regex=True)
#             print('Stock History Data:', df2.to_dict(orient='records'))  # Log the data to inspect
#             return df2.to_json(orient='records')
#         else:
#             return jsonify([])  # Return an empty list if no results
#     except Exception as e:
#         logging.error(f"Error fetching stock history: {e}")
#         return jsonify(error=str(e)), 500
#     finally:
#         session.close()

# if __name__ == '__main__':
#     app.run(debug=True)
