import aiohttp
import asyncio
from . import utils


async def get_item_pages(item_names: list, split: int):
    if split <= 1:
        split = 2
    sublists = utils.split_item_list(item_names, split)
    async with aiohttp.ClientSession() as session:
        tasks = [post_request(sublist, session) for sublist in sublists]
        results = await asyncio.gather(*tasks)
        return results


async def post_request(item_list: list, ses: aiohttp.ClientSession):
    url = "https://growtopia.fandom.com/wiki/Special:Export"
    data = {
        "title": "Special:Export",
        "pages": "\n".join(item_list),
        "curonly": 1,
    }
    async with ses.post(url, data=data) as response:
        result = await response.text()
        return result
