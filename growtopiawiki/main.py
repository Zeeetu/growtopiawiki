import asyncio
from . import scraper, parser, utils
import json


def build_items(**opts):
    asyncio.run(_build_items(**opts))


async def _build_items(**opts):
    if opts.get("items_json"):
        with open(opts["items_json"], "r", encoding="UTF-8") as f:
            items = json.loads(f.read())
    else:
        items = await utils.itemsdat_to_dict(opts.get("items_dat"))
    item_ids_and_names = [(item["id"], item["name"]) for item in items]
    item_names = [item[1] for item in item_ids_and_names]
    raw_pages = await scraper.get_item_pages(item_names, opts.get("split", 5))
    item_dicts = await parser.xmls_to_item_dicts(raw_pages, item_ids_and_names)
    utils.output_to_json(items, item_dicts, **opts)
