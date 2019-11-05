## SEC Filings Web Spider

This spider reads a list of tickers from tickers.csv and inputs the ticker into a starting link. The starting link is the same as searching the ticker on the SEC Edgar database. As an example, go to this [link](https://www.sec.gov/edgar/searchedgar/companysearch.html) and enter a ticker such as MSFT. The next link is [here](https://www.sec.gov/cgi-bin/browse-edgar?CIK=MSFT&owner=exclude&action=getcompany). This is the starting point for all of the spiders. The spider then searchs for keywords such as 8-K, 10-K, and 10-Q. The spider follows the links of the documents button and downloads the first document on the page.

Example documents can be found in the files above.

