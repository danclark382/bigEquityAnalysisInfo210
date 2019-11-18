import scrapy
from scrapy.pipelines.files import FilesPipeline


class SecScrapePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if 'files' in item:
            for file_url, myFile in item['files'].items():
                request = scrapy.Request(url=file_url)
                request.meta['filename'] = myFile
                request.meta['fullPath'] = item['fullPath']
                yield request

    def file_path(self, request, response=None, info=None):
        original_path = super(SecScrapePipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path
        directory = request.meta['fullPath'].split('/')[-1]
        return directory + '/' + request.meta['filename'] + sha1_and_extension
