# Written by Mutlu Polatcan
# 02.12.2019
from scrapy import Spider, Request
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from src.items.book_item import BookItem
from src.utils.constants import Constants


class GoodreadsSpider(Spider):
    name = "goodreads_spider"

    def __init__(self, config):
        super(GoodreadsSpider, self).__init__()
        self.__url = config[Constants.CONFIG_KEY_URL]
        self.__genres = config.get(Constants.CONFIG_KEY_GENRES, None)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super(GoodreadsSpider, cls).from_crawler(crawler, crawler.settings)

    def start_requests(self):
        yield Request(self.__url, callback=self.__genre_urls)

    def __genre_urls(self, response):
        for link in LinkExtractor(allow=Constants.REGEX_GENRES_URL).extract_links(response):
            if self.__genres:
                # Genre filtering
                for genre in self.__genres:
                    if link.url.find(genre) != -1:
                        yield Request(url=link.url, callback=self.__genre_booklists_urls)
            else:
                yield Request(url=link.url, callback=self.__genre_booklists_urls)

    def __genre_booklists_urls(self, response):
        for link in LinkExtractor(allow=Constants.REGEX_GENRES_BOOKLIST_URL).extract_links(response):
            yield Request(url=link.url, callback=self.__genre_booklists_pagination_urls, cb_kwargs={
                Constants.KEY_GENRE_BASE_URL: link.url,
                Constants.KEY_GENRE_TITLE: response.css(Constants.SELECTOR_GENRE_TITLE).get()
            })

    def __genre_booklists_pagination_urls(self, response, **kwargs):
        page_nums = response.css(Constants.SELECTOR_GENRE_PAGINATION).getall()
        page_urls = []

        if len(page_nums) > 0:
            print("List URL: {url}, Last Page Number: {last_page_num}".format(
                url=kwargs[Constants.KEY_GENRE_BASE_URL], last_page_num=page_nums[len(page_nums)-2])
            )

            page_urls = [
                "{base_url}?page={page_num}".format(base_url=kwargs[Constants.KEY_GENRE_BASE_URL], page_num=page_num)
                for page_num in range(1, len(page_nums) + 1)
            ]
        else:
            print("List URL: {url} has a single page".format(url=kwargs[Constants.KEY_GENRE_BASE_URL]))

        for page_url in page_urls:
            yield Request(url=page_url, callback=self.__genre_booklists_book_urls, cb_kwargs=kwargs)

    def __genre_booklists_book_urls(self, response, **kwargs):
        for link in LinkExtractor(allow=Constants.REGEX_GENRES_BOOKLIST_BOOK_URL).extract_links(response):
            yield Request(url=link.url, callback=self.__genre_booklists_book_parse, cb_kwargs=kwargs)

    def __genre_booklists_book_parse(self, response, **kwargs):
        data_text_id = response.css(Constants.SELECTOR_DATA_TEXT_ID).get()
        isbn = response.css(Constants.SELECTOR_BOOK_ISBN).get()

        book = ItemLoader(item=BookItem(), response=response)
        book.add_value(Constants.ITEM_FIELD_GENRE, kwargs[Constants.KEY_GENRE_TITLE])
        book.add_css(Constants.ITEM_FIELD_TITLE, Constants.SELECTOR_BOOK_TITLE)
        book.add_css(Constants.ITEM_FIELD_AUTHOR, Constants.SELECTOR_BOOK_AUTHOR)
        book.add_css(Constants.ITEM_FIELD_RATING, Constants.SELECTOR_BOOK_RATING)
        book.add_css(
            Constants.ITEM_FIELD_DESCRIPTION,
            Constants.SELECTOR_BOOK_DESCRIPTION_LONG.format(data_text_id=data_text_id) if data_text_id else Constants.SELECTOR_BOOK_DESCRIPTION_SHORT
        )
        book.add_css(Constants.ITEM_FIELD_SERIES, Constants.SELECTOR_BOOK_SERIES)
        book.add_css(Constants.ITEM_FIELD_BOOK_FORMAT, Constants.SELECTOR_BOOK_FORMAT)
        book.add_css(Constants.ITEM_FIELD_PAGES, Constants.SELECTOR_BOOK_PAGES)
        book.add_css(Constants.ITEM_FIELD_ISBN, Constants.SELECTOR_BOOK_ISBN if isbn else Constants.SELECTOR_BOOK_ASIN)
        book.add_css(Constants.ITEM_FIELD_EDITION, Constants.SELECTOR_BOOK_EDITION)
        book.add_css(Constants.ITEM_FIELD_EDITION_LANGUAGE, Constants.SELECTOR_BOOK_EDITION_LANGUAGE)
        book.add_css(Constants.ITEM_FIELD_IMAGE_URLS, Constants.SELECTOR_BOOK_COVER_ENLARGE)

        return book.load_item()