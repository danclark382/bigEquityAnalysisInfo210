import json
import pandas as pd
from iexfinance.stocks import Stock
from iexfinance.altdata import get_social_sentiment

IEX_API_VERSION="iexcloud-sandbox"
with open("myKeys.json") as jsonFile:
    data = json.load(jsonFile)
    IEX_TOKEN = data['keys']['iexSandbox']


def parse_csv(tickerCsv="sec_scrape/sec_scrape/tickers.csv"):
    tickerSeries = pd.read_csv(tickerCsv)['Ticker']
    for cmp in tickerSeries:
        a = Stock(cmp, token=IEX_TOKEN)
        df = get_historical_data(cmp, start="20180101", output_format="pandas")
        priceActionFile = cmp + "_priceAction.csv"
        df.to_csv(priceActionFile)
        estimatesFile = cmp + "_estimates.csv"
        df = get_estimates(cmp, output_format="pandas")



parse_csv()