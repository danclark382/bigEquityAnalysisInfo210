# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class SecScrapePipeline(object):
    def process_item(self, item, spider):
        return item

    def file_path(self, request, response=None, info=None):
        original_path = super(SecScrapePipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path
        return request.meta.get('filename','')[0] + "_" + sha1_and_extension