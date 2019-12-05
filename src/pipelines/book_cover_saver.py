# Written by Mutlu Polatcan
# 04.12.2019
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from src.utils.constants import Constants


class BookCoverSaverPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get(Constants.ITEM_FIELD_IMAGE_URLS, []):
            # If book doesn't have ISBN or ASIN don't save that cover photo
            if item.get(Constants.ITEM_FIELD_ISBN, "") != "":
                request = Request(url)
                request.meta[Constants.ITEM_FIELD_GENRE] = item.get(Constants.ITEM_FIELD_GENRE, "")
                request.meta[Constants.ITEM_FIELD_TITLE] = item.get(Constants.ITEM_FIELD_TITLE, "").replace("/", "-")
                request.meta[Constants.ITEM_FIELD_ISBN] = item.get(Constants.ITEM_FIELD_ISBN, "")
                yield request

    def file_path(self, request, response=None, info=None):
        return "{genre}/{title}-{isbn}.jpg".format(
            genre=request.meta[Constants.ITEM_FIELD_GENRE],
            title=request.meta[Constants.ITEM_FIELD_TITLE],
            isbn=request.meta[Constants.ITEM_FIELD_ISBN]
        )
