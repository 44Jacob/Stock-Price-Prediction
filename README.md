# Flask Application for Stock Analysis

This project focuses on developing a Flask application to analyze stock data and provide insights using Python, SQLAlchemy, and machine learning techniques.

Project Setup:

Created a virtual environment named finenv.
Installed essential packages: Flask, SQLAlchemy, NumPy, Pandas, yFinance, TextBlob, and scikit-learn.
Application Structure:

app.py: The core of the Flask application, setting up the web framework and routes.
config.py: Contains configuration variables, including the API key.
api_func.py: Holds custom functions for data fetching and processing.
Main Flask Application (app.py):

Imports necessary libraries for data analysis and machine learning.
Sets up the Flask application and configures SQLAlchemy for database interactions.
Defines a simple home route.
Configuration File (config.py):

Stores the API key and other configuration settings.
API Functions (api_func.py):

Includes functions like get_avg_sentiment_scores, read_data, load_data_to_db, fetch_news, and fetch_all_stock_data to handle data operations and analysis.
Data Processing and Analysis:

Fetches stock data using yFinance.
Interacts with the database using SQLAlchemy.
Performs sentiment analysis with TextBlob.
Uses Linear Regression from scikit-learn for stock price prediction.
Running the Application:

Activate the virtual environment with:
sh
Copy code
source /Users/yakupaltinisik/anaconda3/envs/finenv/bin/activate
Run the Flask application with:
sh
Copy code
flask run
Demonstration:

Live demonstration of the application, showing how to fetch stock data, perform sentiment analysis, and predict stock prices.
Conclusion:

Developed a comprehensive Flask application for stock analysis.
Integrated various Python libraries for data fetching, processing, and machine learning.
Potential future improvements include more advanced models and a more interactive user interface.
