import scrapy
import pandas


# file_urls={
# FILES_STORE='/dclark171/school/pythonfolder/sec_scrapers/sec_files/'
# Enable media pipeline by adding ITEM_PIPELINES setting
# When files are downloaded, the 'files' field will be populated with a list of dictionaries
#    containing information about the downloaded files
# ITEM_PIPELINES = {'scrapy.pipelines.files.FilesPipeline': 1}

class SecScrape(scrapy.Spider):
    name = "sec"

    def start_requests(self):
        urls = [
            'https://www.sec.gov/cgi-bin/browse-edgar?CIK=MSFT&owner=exclude&action=getcompany&Find=Search'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def doc_page(self, response):
        path = 'filepath'
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
