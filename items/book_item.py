from scrapy import Item, Field


class BookItem(Item):
    title = Field()
    author = Field()
    description = Field()
    rating = Field()
    series = Field()
    image_urls = Field()
