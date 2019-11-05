import scrapy
from scrapy.pipelines.files import FilesPipeline

class SecScrapePipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        original_path = super(SecScrapePipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path
        return request.meta.get('filename', '') + "_" + sha1_and_extension

    #def process_item(self, item, spider):
    #    info = self.spiderinfo
    #    requests = self.get_media_requests(item, info)
    #    dlist = [self._process_request(r, info, item) for r in requests]
    #    dfd = DeferredList(dlist, consumeErrors=1)
    #    return dfd.addCallback(self.item_completed, item, info)

    #def get_media_requests(self, item, info):
    #    return [request(x) for x in item.get(self.FILES_URLS_FIELD, [])]