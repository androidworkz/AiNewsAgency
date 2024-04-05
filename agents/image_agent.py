import aiohttp
import logging
from duckduckgo_search import DDGS
from cachetools import TTLCache
from typing import List
from typing import Dict


class ImageAgent:
    def __init__(self, client, cache_ttl: int = 3600):
        self.client = client
        self.cache = TTLCache(maxsize=100, ttl=cache_ttl)

    async def download_image(self, url: str, index: int):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    with open(f"image_{index + 1}.jpg", "wb") as file:
                        file.write(await response.read())
        except aiohttp.ClientError as e:
            logging.error(f"Error downloading image: {e}")
            raise


class ImageAgent:
    def __init__(self, cache_ttl: int = 3600):
        self.cache = TTLCache(maxsize=100, ttl=cache_ttl)

    def retrieve_images(self, topic: str, progress_tracker) -> List[str]:
        progress_tracker.start_task("ImageAgent", "Retrieve Images")
        if topic in self.cache:
            progress_tracker.complete_task("ImageAgent", "Retrieve Images")
            return self.cache[topic]

        image_results = DDGS().images(keywords=topic, max_results=5)
        image_urls = [result["image"] for result in image_results]

        for i, image_url in enumerate(image_urls):
            await self.download_image(image_url, i)


            self.cache[topic] = image_urls
            progress_tracker.complete_task("ImageAgent", "Retrieve Images")
            return image_urls

    async def download_image(self, url: str, index: int):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        filename = f"image_{index + 1}.jpg"
                        with open(filename, "wb") as file:
                            file.write(image_data)
                        logging.info(f"Downloaded image saved as {filename}.")
                    else:
                        logging.error(f"Failed to download image. Status code: {response.status}")
        except aiohttp.ClientError as e:
            logging.error(f"Error downloading image: {e}")
            raise
