# Written by Mutlu Polatcan
# 03.12.2019
import json
import yaml
from sys import argv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from spiders.goodreads_spider import GoodreadsSpider
from spiders.proxy_spider import ProxySpider
from spiders.useragent_spider import UserAgentSpider


class GoodreadsScraper:
    KEY_PROXY = "proxy"
    KEY_USERAGENT = "useragent"
    KEY_GOODREADS = "goodreads"
    KEY_URL = "url"
    KEY_OUTPUT_FILENAME = "output_filename"
    KEY_PROXY_FILENAME = "proxy_filename"
    KEY_USERAGENTS_FILENAME = "useragents_filename"
    KEY_CUSTOM_SETTINGS = "custom_settings"
    KEY_ROTATING_PROXY_LIST = "ROTATING_PROXY_LIST"
    KEY_USER_AGENTS = "USER_AGENTS"

    def __init__(self, config_filename):
        self.__config = yaml.safe_load(open(config_filename, "r"))
        self.__runner = CrawlerRunner()
        self.__proxy_spider_config = self.__config[GoodreadsScraper.KEY_PROXY]
        self.__useragent_spider_config = self.__config[GoodreadsScraper.KEY_USERAGENT]
        self.__goodreads_spider_config = self.__config[GoodreadsScraper.KEY_GOODREADS]

    def __update_goodreads_spider_settings(self):
        GoodreadsSpider.custom_settings = {
            GoodreadsScraper.KEY_ROTATING_PROXY_LIST: json.load(open(self.__goodreads_spider_config[GoodreadsScraper.KEY_PROXY_FILENAME], "r")),
            GoodreadsScraper.KEY_USER_AGENTS: json.load(open(self.__goodreads_spider_config[GoodreadsScraper.KEY_USERAGENTS_FILENAME], "r"))
        }
        GoodreadsSpider.custom_settings.update(self.__goodreads_spider_config[GoodreadsScraper.KEY_CUSTOM_SETTINGS])

    @defer.inlineCallbacks
    def __run_spiders_sequentially(self):
        yield self.__runner.crawl(
            UserAgentSpider,
            self.__useragent_spider_config[GoodreadsScraper.KEY_URL],
            self.__useragent_spider_config[GoodreadsScraper.KEY_OUTPUT_FILENAME]
        )

        yield self.__runner.crawl(
            ProxySpider,
            self.__proxy_spider_config[GoodreadsScraper.KEY_URL],
            self.__proxy_spider_config[GoodreadsScraper.KEY_OUTPUT_FILENAME]
        )

        self.__update_goodreads_spider_settings()

        yield self.__runner.crawl(
            GoodreadsSpider,
            self.__goodreads_spider_config[GoodreadsScraper.KEY_URL]
        )

        reactor.stop()

    def run(self):
        configure_logging()
        self.__run_spiders_sequentially()
        reactor.run()


if __name__ == "__main__":
    GoodreadsScraper(argv[1]).run()