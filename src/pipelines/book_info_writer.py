# Written by Mutlu Polatcan
# 03.12.2019
import re
from src.utils.constants import Constants


class BookInfoWriterPipeline:
    def __init__(self, config):
        self.__config = config

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get(crawler.settings.get(Constants.CONFIG_KEY_OUTPUT_TO)))

    def process_item(self, item, spider):
        item[Constants.ITEM_FIELD_TITLE] = item[Constants.ITEM_FIELD_TITLE][0].strip()
        item[Constants.ITEM_FIELD_SERIES] = item[Constants.ITEM_FIELD_SERIES][0].strip() \
                                              if item.get(Constants.ITEM_FIELD_SERIES, None) is not None \
                                              else ""
        item[Constants.ITEM_FIELD_AUTHOR] = ",".join(item[Constants.ITEM_FIELD_AUTHOR]) \
                                              if len(item[Constants.ITEM_FIELD_AUTHOR]) > 1 \
                                              else item[Constants.ITEM_FIELD_AUTHOR][0].strip()
        item[Constants.ITEM_FIELD_GENRE] = item[Constants.ITEM_FIELD_GENRE][0].strip()
        item[Constants.ITEM_FIELD_RATING] = item[Constants.ITEM_FIELD_RATING][0].strip()
        item[Constants.ITEM_FIELD_DESCRIPTION] = re.sub(
            re.compile(Constants.HTML_REGEX), "", item[Constants.ITEM_FIELD_DESCRIPTION][0].strip().replace("\n", "")
        ) if item.get(Constants.ITEM_FIELD_DESCRIPTION, None) is not None else ""

        if self.__config[Constants.CONFIG_KEY_OUTPUT_TYPE] == "csv":
            file = open(self.__config[Constants.CONFIG_KEY_FILENAME], "a+")

            file.write("\"{}\"\n".format("\"{delim}\"".format(delim=self.__config[Constants.CONFIG_KEY_DELIMITER]).join([
                item[Constants.ITEM_FIELD_TITLE],
                item[Constants.ITEM_FIELD_SERIES],
                item[Constants.ITEM_FIELD_AUTHOR],
                item[Constants.ITEM_FIELD_GENRE],
                item[Constants.ITEM_FIELD_RATING],
                item[Constants.ITEM_FIELD_DESCRIPTION]
            ])))

            file.close()

        return item
