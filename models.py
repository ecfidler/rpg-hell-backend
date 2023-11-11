from pydantic import BaseModel

class Object(BaseModel):
    id: int = 0
    name: str
    effect: str = None
    req = []

    def __init__(self, _name: str, _effect: str, _req=[]):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.req = _req

    def return_data(self):
        info = self.easy_data()
        self.update_info(info)
        return info

    def update_info(self, info):
        # this is a way to easily update other stuff
        pass

    def easy_data(self):
        return ({"id": self.id, "name": self.name, "effect": self.effect, "req": self.req})


class Trait(Object):
    dice: int
    is_passive: bool = False

    def __init__(self, _name: str, _effect: str, _req, _dice: int, _is_passive=False):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.dice = int(_dice)
        self.is_passive = bool(_is_passive)
        if self.dice == 0:
            self.is_passive = True

        self.req = _req

    def update_info(self, info):
        info["dice"] = self.dice
        info["is_passive"] = self.is_passive


class Item(Object):
    cost: int = 0
    craft: int = 0
    tags = []

    def __init__(self, _name: str, _effect: str, _cost: int, _craft: int, _tags, _req=[]):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.cost = int(_cost)
        self.craft = int(_craft)
        self.tags = _tags

        self.req = _req

    def update_info(self, info):
        info["cost"] = self.cost
        info["craft"] = self.craft
        info["tags"] = self.tags


class Spell(BaseModel):
    id: int = 0
    name: str
    effect: str = None
    dice: int = 0
    level: int = 0
    tags = []

    def __init__(self, _name: str, _effect: str, _dice: int, _level: int, _tags):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.dice = int(_dice)
        self.level = int(_level)
        self.tags = _tags

    def return_data(self):
        return {"id": self.id, "name": self.name, "effect": self.effect, "dice": self.dice, "level": self.level, "tags": self.tags}
