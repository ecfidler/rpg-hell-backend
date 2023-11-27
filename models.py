from pydantic import BaseModel


class Object(BaseModel):
    id: int = 0
    name: str
    effect: str = None
    req: list[str] = []

    # def __init__(self, _name: str, _effect: str, _req=[]):
    #     self.name = str(_name).lower()
    #     self.effect = str(_effect)
    #     self.req = _req

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

    # def __init__(self, _name: str, _effect: str, _req, _dice: int, _is_passive=False):
    #     self.name = str(_name).lower()
    #     self.effect = str(_effect)
    #     self.dice = int(_dice)
    #     self.is_passive = bool(_is_passive)
    #     if self.dice == 0:
    #         self.is_passive = True

    #     self.req = _req

    def update_info(self, info):
        info["dice"] = self.dice
        info["is_passive"] = self.is_passive


class Item(Object):
    cost: int = 0
    craft: int = 0
    tags: list[str] = []
    # def __init__(self, _name: str, _effect: str, _cost: int, _craft: int, _tags, _req=[]):
    #     self.name = str(_name).lower()
    #     self.effect = str(_effect)
    #     self.cost = int(_cost)
    #     self.craft = int(_craft)
    #     self.tags = _tags

    #     self.req = _req
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
    tags: list[str] = []

    # def __init__(self, _name: str, _effect: str, _dice: int, _level: int, _tags):
    #     self.name = str(_name).lower()
    #     self.effect = str(_effect)
    #     self.dice = int(_dice)
    #     self.level = int(_level)
    #     self.tags = _tags

    def return_data(self):
        return {"id": self.id, "name": self.name, "effect": self.effect, "dice": self.dice, "level": self.level, "tags": self.tags}


class DBUser(BaseModel):
    id: int = 0
    discord_id: int
    username: str
    email: str
    is_admin: bool = False
    avatar_url: str = ""

    def compare(self,other_user: dict):
        """
        This is used souly for the use of checking to see if we need to update users
        """
        # You shouldent be able to change your discord id
        # if self.discord_id != other_user["discord_id"]:
        #     return False
        if self.username != other_user["username"]:
            return False
        if self.email != other_user["email"]:
            return False
        
        return True

class Creature(BaseModel):
    id: int = 0
    name: str
    types: list[str] = []
    level: int = 0
    body: int = 0
    mind: int = 0
    soul: int = 0
    arcana: int = 0
    crafting: int = 0
    charm: int = 0
    thieving: int = 0
    nature: int = 0
    medicine: int = 0
    traits: list[str] = []
    spells: list[str] = []
    items: list[str] = []
    notes: str = ""

    def output_json(self):
        return {"name": self.name}
    
    def create_textlist_from_Obj(lst):
        txt = ""
        for line in lst:
            txt += f", {line.name}"
        return txt[2:] # lop off the first "", ""

    def create_textlist_from_strlist(lst):
        print(lst)
        print(', '.join(lst))
        return ', '.join(lst)

