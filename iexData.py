import json
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os


with open("myKeys.json") as jsonFile:
    data = json.load(jsonFile)
    IEX_TOKEN = data['keys']['iex']

DATADIR = os.path.exists('data')

def generateStock(ticker):
    """Generate stock object to return

	 Create a stock object from ticker to call iex functions
	 :param ticker: Stock ticker
	 :type ticker: String
	 :return: stock object
	 :return type: iexfinance.stocks.Stock()
	 """
    return Stock(ticker, token=IEX_TOKEN)

def getPriceHistory(ticker):
    """Get the price history of ticker

    Get the historical prices of a ticker starting from startDate through endDate.
	 Conver the dataframe to a CSV and save the file to a directory data/{ticker}/{ticker}.csv.
	 If the directory data or data/ticker does not exit, make the directory.
    :param ticker: Stock ticker
    :type ticker: String
    :return: df of price history
    :return type: Dataframe()
    """
    startDate = datetime(2015, 1, 1)
    endDate = datetime(2019, 12, 25)
    df = get_historical_data(ticker, start=startDate, end=endDate, output_format='pandas', token=IEX_TOKEN)
    if not DATADIR:
        os.makedirs('data')
        os.makedirs('data/' + ticker)
        DATADIR = True
    elif not os.path.exists('data/' + ticker):
        os.makedirs('data/' + ticker)
    filename = 'data/' + ticker + '/' + ticker + '.csv'
    df.to_csv(filename)
    return df

def plotDf(df, ticker):
    """Create a plot of the df timeseries
    
    Generates a matplot chart of the stocks price history based on closing price
    :param df: Timeseries of stock price history
    :type df: Dataframe()
    :return: True
    :return type: Boolean
    """
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'])])
    fig.update_layout(
        title=ticker,
        yaxis_title='Price($)',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False
    )
    fig.show()
    fig.write_image('data/' + ticker + '/' + ticker + '.jpeg')
    return True


def getHeadlines(stock, ticker):
    """Call IEX get_news to gather recent headlines for ticker.

    This method gets the most recent headlines for a ticker
    :param ticker: Stock ticker to search for
    :type ticker: String
    :return: dictionary consisting of (date, headline) key, value pairs
    :return type: dictionary"""
    # get_news() returns a list of dictionaries
    headlines = stock.get_news()
    return headlines

def dataImport():
    """Main entry point for iexData

    This method calls all functions that generate data and pipeline it to the respective directory.
    """
    stockList = pd.read_csv('sec_scrape/tickers.csv')
    for stockTicker in stockList['Ticker']:
        iexStock = generateStock(stockTicker)
        priceDf = getPriceHistory(stockTicker)
        #plotDf(priceDf, stockTicker)
        #getHeadlines(iexStock, stockTicker)
        break

dataImport()
