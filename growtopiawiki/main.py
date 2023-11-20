from . import scraper, parser, utils
import asyncio
import json


def build_items(**kwargs) -> list:
    """
    Build items.dat to a .json file.
    On default will look for items.dat in AppData/Local/Growtopia/cache

    Returns
    ----------------
    Built dictionary

    Kwarg Parameters
    ----------------
    items_dat: str
        Path to items.dat file.
    items_json: str
        Path to already parsed items.dat in json format.
    split: int
        The amount of requests to split items to.
    output: str
        Absolute folder path for items.json output.
    bytearrays: bool
        Whether or not to keep bytearrays in items.json file. (not recommended)
    """
    return asyncio.run(_build_items(**kwargs))


async def _build_items(**kwargs):
    if kwargs.get("items_json"):
        with open(kwargs["items_json"], "r", encoding="UTF-8") as f:
            items = json.loads(f.read())
    else:
        items = await utils.itemsdat_to_dict(
            kwargs.get("items_dat"), kwargs.get("bytearrays", False)
        )
    item_ids_and_names = [(item["id"], item["name"]) for item in items]
    item_names = [item[1] for item in item_ids_and_names]
    raw_pages = await scraper.get_item_pages(item_names, kwargs.get("split", 5))
    item_dicts = await parser.xmls_to_item_dicts(raw_pages, item_ids_and_names)
    return utils.output_to_json(items, item_dicts, **kwargs)
