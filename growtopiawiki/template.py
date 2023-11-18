class TemplateParser:
    def __init__(self, item_names_and_ids):
        self.names_and_ids = item_names_and_ids

    async def itemid_from_name(self, name):
        for item in self.names_and_ids:
            if item[1] == name:
                return int(item[0])

    async def item(self, t):
        description = str(t.get(1).value)
        chi = (
            str(t.get(2, "None")) if str(t.get(2, "None")) not in ["", "0"] else "None"
        )
        return description, chi

    async def splice(self, t):
        ingredients = t.params
        return (
            await self.itemid_from_name(str(ingredients[0])),
            await self.itemid_from_name(str(ingredients[1])),
        )

    async def func(self, t):
        return str(t.params[0])
