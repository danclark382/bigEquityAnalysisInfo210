import csv
from iexfinance.stocks import Stock


def get_stock(ticker):
    stock = Stock(ticker, output_format='pandas', token='sk_e055e4da353343a5ada52ed1f9ac42ca')
    stock.to_csv(ticker + '.csv')
    
    
