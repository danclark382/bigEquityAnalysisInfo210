from scrapy.pipelines.files import FilesPipeline

class SecScrapePipeline(FilesPipeline):
	
	 def process_item(self, item, spider):
	     #if item.get('myFile'):
		  # info = self.spiderinfo
		  # Irequests = arg_to_iter(self.get_media_requests(item, info))
		  # dlist = [self._process_request(r, info, item) for r in requests]
		  # dfd = DeferredList(dlist, consumeErrors=1)
		  # return dfd.addCallback(self.item_completed, item, info)


    def file_path(self, request, response=None, info=None):
        original_path = super(SecScrapePipeline, self).file_path(request, response=None, info=None)
        #filename = 'MSFT_' + response.xpath('(//tr/td)[2]//text()').get() + '_' + response.xpath('.//div[contains(@class, "formContent")]').xpath('.//div[contains(@class, "info")][2]//text()').get()
        sha1_and_extension = original_path.split('/')[1]  # delete 'full/' from the path
        return request.meta.get('filename', '') + "_" + sha1_and_extension
