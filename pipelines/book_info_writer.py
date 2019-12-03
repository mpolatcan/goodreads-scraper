# Written by Mutlu Polatcan
# 03.12.2019
import re


class BookInfoWriterPipeline:
    KEY_AUTHOR = "author"
    KEY_DESCRIPTION = "description"
    KEY_TITLE = "title"
    KEY_RATING = "rating"
    KEY_SERIES = "series"
    KEY_IMAGE_URLS = "image_urls"
    HTML_REGEX = "<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});"

    def __init__(self):
        self.__file = None

    def process_item(self, item, spider):
        item[BookInfoWriterPipeline.KEY_TITLE] = item[BookInfoWriterPipeline.KEY_TITLE][0].strip()
        item[BookInfoWriterPipeline.KEY_SERIES] = item[BookInfoWriterPipeline.KEY_SERIES][0].strip() \
                                              if item.get(BookInfoWriterPipeline.KEY_SERIES, None) is not None \
                                              else ""
        item[BookInfoWriterPipeline.KEY_AUTHOR] = ",".join(item[BookInfoWriterPipeline.KEY_AUTHOR]) \
                                              if len(item[BookInfoWriterPipeline.KEY_AUTHOR]) > 1 \
                                              else item[BookInfoWriterPipeline.KEY_AUTHOR][0].strip()
        item[BookInfoWriterPipeline.KEY_RATING] = item[BookInfoWriterPipeline.KEY_RATING][0].strip()

        item[BookInfoWriterPipeline.KEY_DESCRIPTION] = re.sub(
            re.compile(BookInfoWriterPipeline.HTML_REGEX), "", item[BookInfoWriterPipeline.KEY_DESCRIPTION][0].strip()
        ) if item.get(BookInfoWriterPipeline.KEY_DESCRIPTION, None) is not None else ""

        file = open("books.csv", "a+")

        file.write("\"{}\"\n".format("\"|\"".join([
            item[BookInfoWriterPipeline.KEY_TITLE],
            item[BookInfoWriterPipeline.KEY_SERIES],
            item[BookInfoWriterPipeline.KEY_AUTHOR],
            item[BookInfoWriterPipeline.KEY_RATING],
            item[BookInfoWriterPipeline.KEY_DESCRIPTION]
        ])))

        file.close()

        return item
