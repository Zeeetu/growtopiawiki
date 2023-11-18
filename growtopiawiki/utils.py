from growtopia import ItemsData
import json
import os


def find_itemsdat():
    appdata = os.getenv("LOCALAPPDATA")
    itemspath = os.path.join(appdata, "Growtopia\cache\items.dat")
    return itemspath


def verify_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def output_to_json(items: list, itemwikis: list, **kwargs):
    for item in items:
        for index, itemwiki in enumerate(itemwikis):
            if item["name"] == itemwiki["name"]:
                item.update(itemwikis.pop(index))
    output_path = kwargs.get("output", os.path.join(os.getcwd(), "output"))
    verify_path(output_path)
    with open(os.path.join(output_path, "items.json"), "w+") as file:
        json.dump(items, file, indent=4)


async def itemsdat_to_dict(itemsdat: str = None, bytearrays: bool = False):
    if not itemsdat:
        itemsdat = find_itemsdat()
    raw_items = await _parse_itemsdat(itemsdat)
    item_list = []
    for item in raw_items.items:
        item_data = {}
        for key, value in vars(item).items():
            if isinstance(value, bytearray):
                if bytearrays:
                    item_data[key] = list(value)
            else:
                item_data[key] = value
        item_list.append(item_data)
    return item_list


async def _parse_itemsdat(itemsdat):
    raw_items = ItemsData(itemsdat)
    await raw_items.parse()
    return raw_items


def split_item_list(item_names: list, split_to: int):
    sublist_size = len(item_names) // split_to

    sublists = []

    for i in range(split_to):
        start_index = i * sublist_size
        end_index = (i + 1) * sublist_size if i < split_to - 1 else None
        sublist = item_names[start_index:end_index]
        sublists.append(sublist)

    return sublists
