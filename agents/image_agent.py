import asyncio
import logging
import aiohttp
from duckduckgo_search import ddg_images
from cachetools import TTLCache
from typing import List
from aiohttp import ClientSession, ClientError


async def download_image(url: str, index: int):
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

    async def retrieve_images(self, topic: str, progress_tracker) -> List[str]:
        progress_tracker.start_task("ImageAgent", "Retrieve Images")
        if topic in self.cache:
            progress_tracker.complete_task("ImageAgent", "Retrieve Images")
            return self.cache[topic]

        try:
            image_results = ddg_images(topic, max_results=5)
            image_urls = [result["image"] for result in image_results]

            tasks = []
            for i, image_url in enumerate(image_urls):
                task = asyncio.ensure_future(download_image(image_url, i))
                tasks.append(task)

            await asyncio.gather(*tasks)
            self.cache[topic] = image_urls
            progress_tracker.complete_task("ImageAgent", "Retrieve Images")
            return image_urls
        except IOError as e:
            logging.error(f"Error downloading images: {e}")
            raise
