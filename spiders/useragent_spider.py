# Written by Mutlu Polatcan
# 02.12.2019

from scrapy import Spider, Request
import json


class UserAgentSpider(Spider):
    name = "useragent_spider"
    SELECTOR_USER_AGENT = "div[id=liste] ul a::text"

    def __init__(self, url, useragents_filename):
        super(UserAgentSpider, self).__init__()
        self.__url = url
        self.__useragents_filename = useragents_filename

    def start_requests(self):
        yield Request(url=self.__url, callback=self.parse)

    def parse(self, response):
        user_agents = []

        for row in response.css(UserAgentSpider.SELECTOR_USER_AGENT).getall():
            user_agents.append(row)

        json.dump(user_agents, open(self.__useragents_filename, "w"))
