import scrapy
import csv
from scrapy.loader import ItemLoader
from sec_scrape.items import SecScrapeItem

class SecScrape(scrapy.Spider):
    name = "sec"

    def start_requests(self):
        urls = []
        with open("tickers.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                file = f'https://www.sec.gov/cgi-bin/browse-edgar?CIK={row[0]}&owner=exclude&action=getcompany&Find=Search'
                urls.append(file)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def doc_page(self, response):
        tr = response.xpath('//tr/td/a').attrib['href']
        if tr is not None:
            next_page = response.urljoin(tr)
            try:
                filename = 'MSFT_' + response.xpath('(//tr/td)[2]//text()').get() + '_' + response.xpath('.//div[contains(@class, "formContent")]').xpath('.//div[contains(@class, "info")][2]//text()').get()
            except TypeError:
                filename = ''
            loader = ItemLoader(item=SecScrapeItem(), selector=next_page)
            loader.add_value('file_urls', next_page)
            if filename:
                loader.add_value('myFile', filename)
            yield loader.load_item()

    def parse(self, response):
        tr = response.xpath('//tr')
        next_page = ''
        for td in tr.xpath('.//a[contains(@id, "documentsbutton")]'):
            next_page = td.attrib['href']
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(url=next_page, callback=self.doc_page)

