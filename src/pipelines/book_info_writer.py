# Written by Mutlu Polatcan
# 03.12.2019
import re
from src.utils.constants import Constants


class BookInfoWriterPipeline:
    def __init__(self):
        self.__file = None

    def process_item(self, item, spider):
        item[Constants.ITEM_FIELD_TITLE] = item[Constants.ITEM_FIELD_TITLE][0].strip()
        item[Constants.ITEM_FIELD_SERIES] = item[Constants.ITEM_FIELD_SERIES][0].strip() \
                                              if item.get(Constants.ITEM_FIELD_SERIES, None) is not None \
                                              else ""
        item[Constants.ITEM_FIELD_AUTHOR] = ",".join(item[Constants.ITEM_FIELD_AUTHOR]) \
                                              if len(item[Constants.ITEM_FIELD_AUTHOR]) > 1 \
                                              else item[Constants.ITEM_FIELD_AUTHOR][0].strip()
        item[Constants.ITEM_FIELD_RATING] = item[Constants.ITEM_FIELD_RATING][0].strip()

        item[Constants.ITEM_FIELD_DESCRIPTION] = re.sub(
            re.compile(Constants.HTML_REGEX), "", item[Constants.ITEM_FIELD_DESCRIPTION][0].strip()
        ) if item.get(Constants.ITEM_FIELD_DESCRIPTION, None) is not None else ""

        file = open("books.csv", "a+")

        file.write("\"{}\"\n".format("\"|\"".join([
            item[Constants.ITEM_FIELD_TITLE],
            item[Constants.ITEM_FIELD_SERIES],
            item[Constants.ITEM_FIELD_AUTHOR],
            item[Constants.ITEM_FIELD_RATING],
            item[Constants.ITEM_FIELD_DESCRIPTION]
        ])))

        file.close()

        return item
