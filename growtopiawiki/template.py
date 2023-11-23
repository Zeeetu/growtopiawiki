class TemplateParser:
    def __init__(self, item_names_and_ids: dict):
        self.names_and_ids = item_names_and_ids

    async def itemid_from_name(self, name):
        return self.names_and_ids.get(str(name))

    async def item(self, t):
        description = str(t.get(1).value)
        chi = (
            str(t.get(2, "None")) if str(t.get(2, "None")) not in ["", "0"] else "None"
        )
        return description, chi

    async def splice(self, t):
        ingredients = [str(param) for param in t.params]
        return (
            await self.itemid_from_name(ingredients[0]),
            await self.itemid_from_name(ingredients[1]),
        )

    async def combine(self, t):
        full_recipe = {}
        params = [str(param) for param in t.params if param != ""]
        ingredients = [await self.itemid_from_name(i) for i in params[:6:2]]
        counts = [int(i) for i in params[1:6:2]]

        full_recipe = {
            "recipe": [item for pair in zip(ingredients, counts) for item in pair],
            "yields": int(1 if t.get(7, 1) == "" else str(t.get(7, 1))),
            "combiner": await self.itemid_from_name(t.get(8)) if t.get(8, 0) else None,
        }
        return {k: v for k, v in full_recipe.items() if v is not None}

    async def func(self, t):
        return str(t.params[0])

    async def pet(self, t):
        params = [str(param) for param in t.params]
        return {
            "element": params[1],
            "attack": {"name": params[2], "desc": params[3]},
            "cooldown": int(str(t.get(5, 0)).replace("s", "")),
        }
