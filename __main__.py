import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from unsplash_crawler.spiders.unsplashcom import UnsplashcomSpider
from scrapy.utils.project import get_project_settings


_LOGGER = logging.getLogger(__name__)


def main():
    configure_logging()

    settings = get_project_settings()

    _LOGGER.info("Initialzing crawler")
    install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    process = CrawlerProcess(get_project_settings())
    process.crawl(
        UnsplashcomSpider,
        allowed_domains=settings["ALLOWED_DOMAINS"],
        start_urls=[
            settings["START_URL_PATTERN"].format(category=settings["CRAWL_CATEGORY"])
        ],
    )

    _LOGGER.info("Starting crawler")
    process.start()


if __name__ == "__main__":
    main()
