import xml.etree.ElementTree as ET
import mwparserfromhell as mwp
from . import template
import asyncio

namespace = {"mw": "http://www.mediawiki.org/xml/export-0.11/"}


async def parse_item_page(item_name, item_page, ids_names):
    item_data = {"name": item_name, "function": {}, "recipe": {}}
    parsed_page = mwp.parse(item_page)
    templates = parsed_page.filter_templates()
    parser = template.TemplateParser(ids_names)
    for t in templates:
        match t.name:
            case "Item":
                item_data["desc"], item_data["chi"] = await parser.item(t)
            case "RecipeSplice":
                item_data["recipe"]["splice"] = await parser.splice(t)
            case "RecipeCombine":
                item_data["recipe"]["combine"] = await parser.combine(t)
            case "Added":
                item_data["function"]["add"] = await parser.func(t)
            case "Removed":
                item_data["function"]["rem"] = await parser.func(t)
            case "Pet":
                item_data["pet"] = await parser.pet(t)
            case _:
                ...
    empty_keys = [key for key in item_data.keys() if len(item_data[key]) == 0]
    for key in empty_keys:
        del item_data[key]
    return item_data


async def parse_xml_page(raw_page, item_ids_names):
    item_data_for_page = []
    tree = ET.fromstring(raw_page)
    pages = tree.iter("{" + namespace["mw"] + "}page")
    tasks = [
        parse_item_page(
            item_page.find(".//mw:title", namespace).text,
            item_page.find(".//mw:text", namespace).text,
            item_ids_names,
        )
        for item_page in pages
    ]
    item_data_for_page = await asyncio.gather(*tasks)
    return item_data_for_page


async def xmls_to_item_dicts(raw_pages: list, item_ids_names: list):
    item_dicts = []
    tasks = [parse_xml_page(raw_page, item_ids_names) for raw_page in raw_pages]
    results = await asyncio.gather(*tasks)
    for result in results:
        item_dicts.extend(result)
    return item_dicts
