# Written by Mutlu Polatcan
# 03.12.2019
import json
import yaml
from sys import argv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from src.spiders.goodreads_spider import GoodreadsSpider
from src.spiders.proxy_spider import ProxySpider
from src.spiders.useragent_spider import UserAgentSpider
from src.utils.constants import Constants


class GoodreadsScraper:
    def __init__(self, config_filename):
        self.__config = yaml.safe_load(open(config_filename, "r"))
        self.__runner = CrawlerRunner()
        self.__proxy_spider_config = self.__config[Constants.KEY_PROXY]
        self.__useragent_spider_config = self.__config[Constants.KEY_USERAGENT]
        self.__goodreads_spider_config = self.__config[Constants.KEY_GOODREADS]

    def __update_goodreads_spider_settings(self):
        GoodreadsSpider.custom_settings = {
            Constants.KEY_ROTATING_PROXY_LIST: json.load(open(self.__goodreads_spider_config[Constants.KEY_PROXY_FILENAME], "r")),
            Constants.KEY_USER_AGENTS: json.load(open(self.__goodreads_spider_config[Constants.KEY_USERAGENTS_FILENAME], "r"))
        }
        GoodreadsSpider.custom_settings.update(self.__goodreads_spider_config[Constants.KEY_CUSTOM_SETTINGS])

    @defer.inlineCallbacks
    def __run_spiders_sequentially(self):
        yield self.__runner.crawl(UserAgentSpider, self.__useragent_spider_config)
        yield self.__runner.crawl(ProxySpider, self.__proxy_spider_config)

        self.__update_goodreads_spider_settings()

        yield self.__runner.crawl(GoodreadsSpider, self.__goodreads_spider_config)

        reactor.stop()

    def run(self):
        configure_logging()
        self.__run_spiders_sequentially()
        reactor.run()


if __name__ == "__main__":
    GoodreadsScraper(argv[1]).run()
