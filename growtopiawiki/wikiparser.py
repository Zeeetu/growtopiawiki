from growtopia import ItemsData
import xml.etree.ElementTree as ET
import mwparserfromhell
import aiohttp
import asyncio
import json
import os


class WikiParser:
    def __init__(self, **options):
        self.options = options
        if self.options.get("items_json"):
            self._items_json_path = self.options.get("items_json")
        else:
            self._items_dat_path = self.options.get("items_dat", self._findItemsDat())
            self._itemsdat = self._parseItemsDat()
            self._items_json_path, self._item_list = self._itemsToJson()
        self._item_names_with_ids = self._getItemNamesAndIDS()

        self._split_names = None
        self._namespace = {"mw": "http://www.mediawiki.org/xml/export-0.11/"}

    def wikiToJson(self, split=5):
        asyncio.run(self._wikiToJson(split))

    async def _getItemIDFromName(self, name):
        for item in self._item_names_with_ids:
            if item[1].lower() == name.lower():
                return item[0]

    async def _wikiToJson(self, split):
        all_item_data = []
        self._split_names = await self._splitItems(split)
        _raw_pages = await self._sendSplitItems()
        tasks = [self._parseXML(xmlpage) for xmlpage in _raw_pages]
        results = await asyncio.gather(*tasks)
        for result in results:
            for subresult in result:
                all_item_data.append(subresult)
        for item in self._item_list:
            for itemdata in all_item_data:
                if item["name"] == itemdata["name"]:
                    itemdata.pop("name")
                    item["info"] = itemdata
                    all_item_data.remove(itemdata)
        with open(self._items_json_path, "w+", encoding="UTF-8") as file:
            json.dump(self._item_list, file, indent=4, ensure_ascii=False)

    async def _parseXML(self, xmldata):
        item_data_for_page = []
        tree = ET.fromstring(xmldata)
        for itempage in tree.iter("{" + self._namespace["mw"] + "}page"):
            item_name = itempage.find(".//mw:title", self._namespace).text
            page_text = itempage.find(".//mw:text", self._namespace).text
            item_data = await self._parsePage(item_name, page_text)
            item_data_for_page.append(item_data)
        return item_data_for_page

    async def _parsePage(self, itemname, page):
        data = {}
        templates = mwparserfromhell.parse(page).filter_templates()
        data["name"] = str(itemname)
        for template in templates:
            if template.name == "Item":
                data["desc"], data["chi"] = await self._itemTemplate(template)
            elif template.name == "RecipeSplice":
                data["recipe_splice"] = await self._spliceTemplate(template)
            elif template.name == "RecipeCombine":
                data["recipe_combine"] = await self._combineTemplate(template)
            elif template.name == "Added":
                data["equip"] = await self._addFuncTemplate(template)
            elif template.name == "Removed":
                data["unequip"] = await self._remFuncTemplate(template)
            else:
                pass
                # add support for other data (ex. consumable recipe)
                # print(itemname, template)
        return data

    async def _remFuncTemplate(self, t):
        return str(t.params[0])

    async def _addFuncTemplate(self, t):
        return str(t.params[0])

    async def _combineTemplate(self, t):
        params = list(filter(None, t.params))
        ingredientList = [
            (await self._getItemIDFromName(str(params[i])), 1)
            for i in range(0, len(params) - 1, 2)
        ]
        if len(params) % 2 != 0:
            ingredientList.append(str(params[-1]))
        return ingredientList

    async def _spliceTemplate(self, t):
        return (
            await self._getItemIDFromName(str(t.params[0])),
            await self._getItemIDFromName(str(t.params[1])),
        )

    async def _itemTemplate(self, t):
        description = t.get(1).value
        chi = (
            str(t.get(2, "None")).lower()
            if str(t.get(2, "None")).lower() not in ["", "0"]
            else "None"
        )
        return str(description), str(chi)

    async def _postReq(self, query):
        url = "https://growtopia.fandom.com/wiki/Special:Export"
        data = {
            "title": "Special:Export",
            "pages": "\n".join(query),
            "curonly": 1,
        }
        async with self.ses.post(url, data=data) as response:
            result = await response.text()
            return result

    async def _sendSplitItems(self):
        async with aiohttp.ClientSession() as self.ses:
            tasks = [self._postReq(query) for query in self._split_names]
            results = await asyncio.gather(*tasks)
            return results

    async def _splitItems(self, split):
        k, m = divmod(len(self._item_names_with_ids), split)
        return [
            [
                name
                for _, name in self._item_names_with_ids[
                    i * k + min(i, m) : (i + 1) * k + min(i + 1, m)
                ]
            ]
            for i in range(split)
        ]

    def _getItemNamesAndIDS(self):
        with open(self._items_json_path, "r") as raw:
            self._items = json.loads(raw.read())
        return [(item["id"], item["name"]) for item in self._items]

    def _findItemsDat(self):
        _appdata = os.getenv("LOCALAPPDATA")
        _itemspath = os.path.join(_appdata, "Growtopia\cache\items.dat")
        return _itemspath

    def _parseItemsDat(self):
        _itemsdat = ItemsData(self._items_dat_path)
        asyncio.run(_itemsdat.parse())
        return _itemsdat

    def _verifyPath(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _itemsToJson(self):
        _item_list = []
        _output_path = os.path.join(os.getcwd(), "output")
        self._verifyPath(_output_path)
        _keep_byterrays = self.options.get("bytearrays", False)
        for item in self._itemsdat.items:
            _item_data = {}
            for key, value in vars(item).items():
                if isinstance(value, bytearray):
                    if _keep_byterrays:
                        _item_data[key] = list(value)
                else:
                    _item_data[key] = value
            _item_list.append(_item_data)
        with open(os.path.join(_output_path, "items.json"), "w+") as file:
            json.dump(_item_list, file, indent=4)
            return file.name, _item_list
