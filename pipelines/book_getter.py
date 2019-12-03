import re


class BookGetterPipeline:
    KEY_AUTHOR = "author"
    KEY_DESCRIPTION = "description"
    KEY_TITLE = "title"
    KEY_RATING = "rating"
    KEY_SERIES = "series"
    KEY_IMAGE_URLS = "image_urls"

    def __init__(self):
        self.__file = None

    def open_spider(self, spider):
        self.__file = open("books.txt", "a+")

    def close_spider(self, spider):
        self.__file.close()

    def process_item(self, item, spider):
        item[BookGetterPipeline.KEY_AUTHOR] = ",".join(item[BookGetterPipeline.KEY_AUTHOR]) \
                                              if len(item[BookGetterPipeline.KEY_AUTHOR]) > 1 \
                                              else item[BookGetterPipeline.KEY_AUTHOR][0].strip()
        item[BookGetterPipeline.KEY_DESCRIPTION] = re.sub(
            re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});'),
            '',
            item[BookGetterPipeline.KEY_DESCRIPTION][0]
        )
        item[BookGetterPipeline.KEY_TITLE] = item[BookGetterPipeline.KEY_TITLE][0].strip()
        item[BookGetterPipeline.KEY_RATING] = item[BookGetterPipeline.KEY_RATING][0].strip()
        item[BookGetterPipeline.KEY_SERIES] = item[BookGetterPipeline.KEY_SERIES][0].strip() \
                                              if item.get(BookGetterPipeline.KEY_SERIES, None) is not None \
                                              else ""
        return item
