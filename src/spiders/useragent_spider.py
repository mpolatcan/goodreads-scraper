# Written by Mutlu Polatcan
# 02.12.2019
import json
from scrapy import Spider, Request
from src.utils.constants import Constants


class UserAgentSpider(Spider):
    name = "useragent_spider"

    def __init__(self, config):
        super(UserAgentSpider, self).__init__()
        self.__url = config[Constants.KEY_URL]
        self.__useragents_filename = config[Constants.KEY_OUTPUT_FILENAME]

    def start_requests(self):
        yield Request(url=self.__url, callback=self.parse)

    def parse(self, response):
        user_agents = []

        for row in response.css(Constants.SELECTOR_USER_AGENT).getall():
            user_agents.append(row)

        json.dump(user_agents, open(self.__useragents_filename, "w"))
