import scrapy
import pymongo
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings


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


class MongoDBPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGO_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem(f"Missing {data}!")
            if valid:
                self.collection.inset(dict(item))
                log.msg("Item addded to MongoDB database!",
                        level=log.DEBUG, spider=spider)
            return item
