# Written by Mutlu Polatcan
# 02.12.2019
import json
from scrapy import Spider, Request
from src.utils.constants import Constants


class ProxySpider(Spider):
    name = "proxy_spider"

    def __init__(self, config):
        super(ProxySpider, self).__init__()
        self.__url = config[Constants.CONFIG_KEY_URL]
        self.__proxies_filename = config[Constants.CONFIG_KEY_OUTPUT_FILENAME]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super(ProxySpider, cls).from_crawler(crawler, crawler.settings)

    def start_requests(self):
        yield Request(url=self.__url, callback=self.parse)

    def parse(self, response):
        proxies = []

        for row in response.css(Constants.SELECTOR_PROXY_LIST_ROW):
            proxy_info = row.css(Constants.SELECTOR_PROXY_INFO).getall()

            # If HTTP "yes" then add to proxy list
            if proxy_info[6] == "yes":
                proxies.append("{ip}:{port}".format(ip=proxy_info[0], port=proxy_info[1]))

        json.dump(proxies, open(self.__proxies_filename, "w"))
