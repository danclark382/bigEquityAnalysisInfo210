from iexfinance.stocks import get_historical_data
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def getPriceHistory(ticker):
    """Get the price history of ticker

    Get the historical prices of a ticker starting from startDate through endDate
	 :param ticker: Stock ticker
	 :type ticker: String
	 :return: df of price history
	 :return type: Dataframe()
	 """
    startDate = datetime(2019, 11, 1)
    endDate = datetime(2019, 12, 25)
    token = "sk_a49b63b98e5146f3be136aade0c10b09"
    df = get_historical_data(ticker, start=startDate, end=endDate, output_format='pandas', token=token)
    df.to_csv('priceAction/' + ticker + '.csv')
    return df

def plotDf(df):
    """Create a plot of the df timeseries
    
    Generates a matplot chart of the stocks price history based on closing price
    :param df: Timeseries of stock price history
    :type df: Dataframe()
    :return: True
    :return type: Boolean
    """
    closingSeries = df['close']
    closingSeries.plot()
    plt.figure(); closingSeries.plot();
    plt.show()
    return True

stockList = pd.read_csv('sec_scrape/tickers.csv')
for stock in stockList['TICKER']:
    data = getPriceHistory(stock)
    plotDf(data)
    break
