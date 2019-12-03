import json
import yaml
from sys import argv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from spiders.goodreads_spider import GoodreadsSpider
from spiders.proxy_spider import ProxySpider
from spiders.useragent_spider import UserAgentSpider

if __name__ == "__main__":
    configure_logging()
    runner = CrawlerRunner()
    config = yaml.load(open(argv[1], "r"))
    proxy_spider_config, useragent_spider_config, goodreads_spider_config = config["proxy"], config["useragent"], config["goodreads"]

    @defer.inlineCallbacks
    def crawl_spiders():
        '''
        yield runner.crawl(
            UserAgentSpider,
            useragent_spider_config["url"],
            useragent_spider_config["output_filename"]
        )
        '''

        yield runner.crawl(
            ProxySpider,
            proxy_spider_config["url"],
            proxy_spider_config["output_filename"]
        )

        GoodreadsSpider.custom_settings = {
            'ROTATING_PROXY_LIST': json.load(open(goodreads_spider_config["proxy_filename"], "r")),
            'USER_AGENTS': json.load(open(goodreads_spider_config["useragents_filename"], "r"))
        }
        GoodreadsSpider.custom_settings.update(goodreads_spider_config["custom_settings"])

        yield runner.crawl(GoodreadsSpider, goodreads_spider_config["url"])
        reactor.stop()

    crawl_spiders()
    reactor.run()