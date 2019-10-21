import scrapy
import pandas

class SecScrape(scrapy.Spider):
    name = "sec"

    def start_requests(self):
        urls = [
            'https://www.sec.gov/cgi-bin/browse-edgar?CIK=MSFT&owner=exclude&action=getcompany&Find=Search'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def doc_page(self, response):
        filename = 'MSFT_'response.xpath('.//div[contains(@class, "formContent")]').xpath('.//div[contains(@class, "info")][2]//text()').get()
        tr = response.xpath('//tr/td/a').attrib['href']
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


    def parse(self, response):
        tr = response.xpath('//tr')
        for td in tr.xpath('.//a[contains(@id, "documentsbutton")]'):
            next_page = td.attrib['href']
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.doc_page)
#        page = response.url.split("/")[-1]
#        filename = 'sec-%s.html' % page
#        with open(filename, 'wb') as f:
#            f.write(response.body)
#        self.log('Saved file %s' % filename)