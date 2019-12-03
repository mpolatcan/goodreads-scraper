# Written by Mutlu Polatcan
# 03.12.2019
from scrapy import Item, Field


class BookItem(Item):
    genre = Field()
    title = Field()
    author = Field()
    description = Field()
    rating = Field()
    series = Field()
    image_urls = Field()
