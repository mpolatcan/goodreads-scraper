# Written by Mutlu Polatcan
# 03.12.2019
import re
from src.utils.constants import Constants


class BookInfoWriterPipeline:
    def __init__(self, config):
        self.__config = config
        self.__write_to = {
            Constants.OUTPUT_TYPE_CSV: self.__write_to_csv,
            Constants.OUTPUT_TYPE_MONGO: self.__write_to_mongo,
            Constants.OUTPUT_TYPE_DRIVE: self.__write_to_drive,
            Constants.OUTPUT_TYPE_GCS: self.__write_to_gcs
        }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get(crawler.settings.get(Constants.CONFIG_KEY_OUTPUT_TO)))

    def __write_to_csv(self, item):
        file = open(self.__config[Constants.CONFIG_KEY_FILENAME], "a+")

        file.write("\"{}\"\n".format("\"{delim}\"".format(delim=self.__config[Constants.CONFIG_KEY_DELIMITER]).join([
            item.get(Constants.ITEM_FIELD_TITLE, ""),
            item.get(Constants.ITEM_FIELD_SERIES, ""),
            item.get(Constants.ITEM_FIELD_AUTHOR, ""),
            item.get(Constants.ITEM_FIELD_GENRE, ""),
            item.get(Constants.ITEM_FIELD_RATING, ""),
            item.get(Constants.ITEM_FIELD_DESCRIPTION, ""),
            item.get(Constants.ITEM_FIELD_BOOK_FORMAT, ""),
            item.get(Constants.ITEM_FIELD_EDITION, ""),
            item.get(Constants.ITEM_FIELD_PAGES, ""),
            item.get(Constants.ITEM_FIELD_ISBN, ""),
            item.get(Constants.ITEM_FIELD_EDITION_LANGUAGE, "")
        ])))

        file.close()

    def __write_to_mongo(self, item):
        # TODO Write to Mongo implementation
        print("Writing to MongoDB...")

    def __write_to_drive(self, item):
        # TODO Write to Google Drive implementation
        print("Writing to Google Drive...")

    def __write_to_gcs(self, item):
        # TODO Write to Google Cloud Storage implementation
        print("Writing to Google Cloud Storage...")

    def process_item(self, item, spider):
        item[Constants.ITEM_FIELD_DESCRIPTION] = re.sub(
            re.compile(Constants.HTML_REGEX), "", item.get(Constants.ITEM_FIELD_DESCRIPTION, "").replace("\n", "")
        )
        item[Constants.ITEM_FIELD_PAGES] = item[Constants.ITEM_FIELD_PAGES].split()[0] if item.get(Constants.ITEM_FIELD_PAGES, "") != "" else ""

        # If book doesn't have ISBN or ASIN don't save its info
        if item.get(Constants.ITEM_FIELD_ISBN, "") != "":
            self.__write_to[self.__config[Constants.CONFIG_KEY_OUTPUT_TYPE]](item)

        return item
