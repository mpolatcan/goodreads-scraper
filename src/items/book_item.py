# Written by Mutlu Polatcan
# 03.12.2019
from scrapy import Item, Field
from scrapy.loader.processors import Join


class CustomTakeFirst:
    def __call__(self, values):
        for value in values:
            if value is not None and value != '':
                return value.strip()

        return ""


class BookItem(Item):
    title = Field(output_processor=CustomTakeFirst())
    author = Field(output_processor=Join(separator=", "))
    description = Field(output_processor=CustomTakeFirst())
    genre = Field(output_processor=CustomTakeFirst())
    rating = Field(output_processor=CustomTakeFirst())
    series = Field(output_processor=CustomTakeFirst())
    book_format = Field(output_processor=CustomTakeFirst())
    isbn = Field(output_processor=CustomTakeFirst())
    pages = Field(output_processor=CustomTakeFirst())
    edition = Field(output_processor=CustomTakeFirst())
    edition_language = Field(output_processor=CustomTakeFirst())
    image_urls = Field()
