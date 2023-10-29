import logging
import scrapy
import typing as t

from scrapy.http import HtmlResponse
from unsplash_crawler.items import UnsplashCrawlerItem


_LOGGER = logging.getLogger(__name__)


class UnsplashcomSpider(scrapy.Spider):
    name = "unsplashcom"

    def parse(
        self, response: HtmlResponse
    ) -> t.Generator[UnsplashCrawlerItem, t.Any, t.Any]:
        _LOGGER.info("Processing images for url:  %s", response.url)
        img_container = response.xpath("//div[@data-test='search-photos-route']")
        for fig_div in img_container.xpath(
            "//figure[@data-test='photo-grid-masonry-figure']/div"
        ):
            img_selector = fig_div.xpath(
                "div[1]//img[@data-test='photo-grid-masonry-img']"
            )
            title = img_selector.xpath("@alt")
            url = img_selector.xpath("@srcset")

            tags = fig_div.xpath("div[2]//a/text()")

            yield UnsplashCrawlerItem(title=title, url=url, tags=tags)
