# Written by Mutlu Polatcan
# 02.12.2019
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from items.book_item import BookItem
from scrapy.linkextractors import LinkExtractor


class GoodreadsSpider(Spider):
    name = "goodreads_spider"
    KEY_BASE_URL = "base_url"
    KEY_GENRE_BASE_URL = "genre_base_url"
    KEY_CATEGORY_ENDPOINTS = "category_endpoints"
    KEY_GENRE_TITLE = "genre_title"
    SELECTOR_GENRE_URL = "div[id=browseBox] a[class=gr-hyperlink]::attr(href)"
    SELECTOR_GENRE_TITLE = "div[id=browseBox] a[class=gr-hyperlink]::text"
    SELECTOR_GENRE_BOOKLIST_URL = "a[class=listTitle]::attr(href)"
    SELECTOR_GENRE_PAGINATION = "div[class=pagination] a::text"
    SELECTOR_GENRE_BOOKLIST_BOOK_URL = "a[class=bookTitle]::attr(href)"
    SELECTOR_BOOK_TITLE = "h1[id=bookTitle]::text"
    SELECTOR_BOOK_AUTHOR = "a[class=authorName] span[itemprop=name]::text"
    SELECTOR_BOOK_RATING = "span[itemprop=ratingValue]::text"
    SELECTOR_BOOK_DESCRIPTION = "div[id=description]"
    SELECTOR_BOOK_COVER_ENLARGE = "div[class=editionCover] img::attr(src)"
    SELECTOR_BOOK_SERIES = "h2[id=bookSeries] a::text"

    def __init__(self, url):
        super(GoodreadsSpider, self).__init__()
        self.__url = url

    def start_requests(self):
        yield Request(self.__url, callback=self.__genre_urls)

    def __genre_urls(self, response):
        for link in LinkExtractor(allow=r"/genres/+").extract_links(response):
            yield Request(url=link.url, callback=self.__genre_booklists_urls)

    def __genre_booklists_urls(self, response):
        for link in LinkExtractor(allow=r"/list/show/+").extract_links(response):
            yield Request(url=link.url, callback=self.__genre_booklists_pagination_urls, cb_kwargs={
                GoodreadsSpider.KEY_GENRE_BASE_URL: link.url
            })

    def __genre_booklists_pagination_urls(self, response, **kwargs):
        page_nums = response.css(GoodreadsSpider.SELECTOR_GENRE_PAGINATION).getall()
        page_urls = []

        if len(page_nums) > 0:
            print("List URL: {url}, Last Page Number: {last_page_num}".format(
                url=kwargs[GoodreadsSpider.KEY_GENRE_BASE_URL], last_page_num=page_nums[len(page_nums)-2])
            )

            page_urls = [
                "{base_url}?page={page_num}".format(base_url=kwargs[GoodreadsSpider.KEY_GENRE_BASE_URL], page_num=page_num)
                for page_num in range(1, len(page_nums) + 1)
            ]
        else:
            print("List URL: {url} has a single page".format(url=kwargs[GoodreadsSpider.KEY_GENRE_BASE_URL]))

        for page_url in page_urls:
            yield Request(url=page_url, callback=self.__genre_booklists_book_urls)

    def __genre_booklists_book_urls(self, response):
        for link in LinkExtractor("/book/show/+").extract_links(response):
            yield Request(url=link.url, callback=self.__genre_booklists_book_parse)

    def __genre_booklists_book_parse(self, response):
        book = ItemLoader(item=BookItem(), response=response)
        book.add_css("title", GoodreadsSpider.SELECTOR_BOOK_TITLE)
        book.add_css("author", GoodreadsSpider.SELECTOR_BOOK_AUTHOR)
        book.add_css("rating", GoodreadsSpider.SELECTOR_BOOK_RATING)
        book.add_css("description", GoodreadsSpider.SELECTOR_BOOK_DESCRIPTION)
        book.add_css("series", GoodreadsSpider.SELECTOR_BOOK_SERIES)
        book.add_css("image_urls", GoodreadsSpider.SELECTOR_BOOK_COVER_ENLARGE)

        return book.load_item()