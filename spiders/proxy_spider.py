# Written by Mutlu Polatcan
# 02.12.2019

from scrapy import Spider, Request
import json


class ProxySpider(Spider):
    name = "proxy_spider"
    SELECTOR_PROXY_LIST_ROW = "table[id=proxylisttable] tbody tr"
    SELECTOR_PROXY_INFO = "td::text"

    def __init__(self, url, proxies_filename):
        super(ProxySpider, self).__init__()
        self.__url = url
        self.__proxies_filename = proxies_filename

    def start_requests(self):
        yield Request(url=self.__url, callback=self.parse)

    def parse(self, response):
        proxies = []

        for row in response.css(ProxySpider.SELECTOR_PROXY_LIST_ROW):
            proxy_info = row.css(ProxySpider.SELECTOR_PROXY_INFO).getall()

            if proxy_info[6] == "yes":
                proxies.append("{ip}:{port}".format(ip=proxy_info[0], port=proxy_info[1]))

        json.dump(proxies, open(self.__proxies_filename, "w"))
