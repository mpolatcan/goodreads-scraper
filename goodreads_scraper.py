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
from src.utils.constants import Constants


class GoodreadsScraper:
    def __init__(self, config_filename):
        self.__config = yaml.safe_load(open(config_filename, "r"))
        self.__runner = CrawlerRunner()

    def __load_crawler_settings(self):
        GoodreadsSpider.custom_settings = self.__config[Constants.CONFIG_KEY_GOODREADS]
        ProxySpider.custom_settings = self.__config[Constants.CONFIG_KEY_PROXY]

    @defer.inlineCallbacks
    def __run_spiders_sequentially(self):
        yield self.__runner.crawl(ProxySpider)

        GoodreadsSpider.custom_settings.update({
            Constants.KEY_ROTATING_PROXY_LIST: json.load(open(self.__config[Constants.CONFIG_KEY_PROXY][Constants.CONFIG_KEY_OUTPUT_FILENAME], "r")
        )})

        yield self.__runner.crawl(GoodreadsSpider)

        reactor.stop()

    def run(self):
        configure_logging()
        self.__load_crawler_settings()
        self.__run_spiders_sequentially()
        reactor.run()


if __name__ == "__main__":
    GoodreadsScraper(argv[1]).run()
