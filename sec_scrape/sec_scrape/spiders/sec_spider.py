import scrapy
import csv
from scrapy.loader import ItemLoader
from sec_scrape.items import SecScrapeItem
import os

FILES_STORE = '/Users/dclark171/python/info212/bigEquityAnalysisInfo210/data/'


class SecScrape(scrapy.Spider):
    name = "sec"

    def start_requests(self):
        urls = []
        with open("sec_scrape/tickers.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                # file = f'https://www.sec.gov/cgi-bin/browse-edgar?CIK={row[0]}&owner=exclude&action=getcompany&Find=Search'
                urls.append(row)
                break
        for url in urls:
            #link = f'https://www.sec.gov/cgi-bin/browse-edgar?CIK={url}&owner=exclude&action=getcompany&Find=Search'
            link = f'https://www.sec.gov/cgi-bin/browse-edgar?CIK=AAPL&owner=exclude&action=getcompany&Find=Search'
            scrapedItem = SecScrapeItem(company='AAPL')
            yield scrapy.Request(url=link, callback=self.parse, meta={'item': scrapedItem})

    def doc_page(self, response):
        tr = response.xpath('//tr/td/a').attrib['href']
        stockMeta = SecScrapeItem()
        company = response.meta['item']['company']
        global FILES_STORE
        if tr is not None:
            newDir = FILES_STORE + company
            next_page = response.urljoin(tr)
            try:
                filename = company + '_' + response.xpath('(//tr/td)[2]//text()').get() + '_' + response.xpath('.//div[contains(@class, "formContent")]').xpath('.//div[contains(@class, "info")][2]//text()').get()
                stockMeta['myFile'] = filename
            except TypeError:
                filename = ''
            stockMeta['file_urls'] = next_page
            stockMeta['directory'] = newDir
            stockMeta['company'] = company
            stockMeta['files'] = {next_page: filename}
            yield stockMeta
            yield scrapy.Request(next_page)

    def parse(self, response):
        tr = response.xpath('//tr')
        next_page = ''
        for td in tr.xpath('.//a[contains(@id, "documentsbutton")]'):
            next_page = td.attrib['href']
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(url=next_page, callback=self.doc_page, meta={'item': response.meta['item']})

