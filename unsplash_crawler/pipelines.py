# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import scrapy

from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings


_LOGGER = logging.getLogger(__name__)


class UnsplashCrawlerUnwrapSelectorsPipeline:
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        _LOGGER.info("Prepare item params")

        # prepare url
        item["url"] = item["url"].get().split()[-2]

        # prepare tags
        item["tags"] = [t.get() for t in item["tags"]]

        # return prepared item
        _LOGGER.info("Item params have been prepared")
        return item


class UnsplashCrawlerDownloadImagePipeline(ImagesPipeline):
    def get_media_requests(
        self, item: scrapy.Item, info: scrapy.pipelines.media.MediaPipeline.SpiderInfo
    ):
        image_url = item.get("url")
        _LOGGER.info("Downloading image for url: %s", image_url)

        try:
            yield scrapy.Request(url=image_url)
        except Exception as err:
            raise DropItem(f"Failed to dawnload image with url: `{image_url}`") from err

    def item_completed(
        self,
        results: list[tuple[bool, dict]],
        item: scrapy.Item,
        info: scrapy.pipelines.media.MediaPipeline.SpiderInfo,
    ):
        status, download_info = results[0]
        image_url = item.get("url")

        if not status:
            raise DropItem(f"Failed to dawnload image with url: `{image_url}`")

        _LOGGER.info("Image has been downloaded for url: %s", image_url)
        item["download_path"] = download_info["path"]

        return item


class UnsplashCrawlerStoreDatabasePipeline:
    def __init__(self):
        settings = get_project_settings()

        connection = pymongo.MongoClient(
            host=settings["MONGO_HOST"], port=settings["MONGO_PORT"]
        )
        db = connection[settings["MONGO_DB"]]
        self.collection = db[settings["MONGO_COLLECTION"]]

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        image_url = item["url"]

        if self.collection.count_documents({"url": image_url}) > 0:
            _LOGGER.info("Seems image with url `%s` is already stored", image_url)
            return

        _LOGGER.info("Storing image info has been with url: %s", image_url)
        self.collection.insert_one(
            {
                "url": item.get("url"),
                "tags": item.get("tags"),
                "download_path": item.get("download_path"),
            }
        )
        _LOGGER.info("Image info has been stored with url: %s", image_url)
