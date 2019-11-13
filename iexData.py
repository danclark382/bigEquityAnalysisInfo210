import json
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

print(os.getcwd())

with open("../myKeys.json") as jsonFile:
    data = json.load(jsonFile)
    IEX_TOKEN = data['keys']['iex']


def getPriceHistory(ticker):
    """Get the price history of ticker

    Get the historical prices of a ticker starting from startDate through endDate
    :param ticker: Stock ticker
    :type ticker: String
    :return: df of price history
    :return type: Dataframe()
"""
    startDate = datetime(2015, 1, 1)
    endDate = datetime(2019, 12, 25)
    token = IEX_TOKEN
    df = get_historical_data(ticker, start=startDate, end=endDate, output_format='pandas', token=token)
    filename = 'data/' + ticker + '/' + ticker + '.csv'
    df.to_csv(filename)
    return df

def plotDf(df,ticker):
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


def getHeadlines(ticker):
    """Call IEX get_news to gather recent headlines for ticker.

    This method gets the most recent headlines for a ticker
    :param ticker: Stock ticker to search for
    :type ticker: String
    :return: dictionary consisting of (date, headline) key, value pairs
    :return type: dictionary"""
    headlines = Stock("AAPL", token=IEX_TOKEN)
    head = headlines.get_news()
    print(head)
    print(type(head))


def dataImport():
    """Main entry point for iexData

    This method calls all functions that generate data and pipeline it to the respective directory.
    """
    stockList = pd.read_csv('sec_scrape/tickers.csv')
    for stock in stockList['Ticker']:
        #priceDf = getPriceHistory(stock)
        #plotDf(priceDf, stock)
        getHeadlines(stock)
        break

dataImport()
