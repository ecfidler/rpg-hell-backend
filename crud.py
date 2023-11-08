from translator import Trait, Item, Spell, spliter
import translator as dl  # do_query, create, read_object, read_spell

# open query


def open_query(query: str):
    return dl.do_query(query)


def get_object(id: int):
    return dl.read_object(id)


def object_search(name: str):  # todo: add other search params
    return dl.read_object(name)


def get_spell(id: int):
    return dl.read_spell(id)


def spell_search(name: str):  # todo: add other search params
    return dl.read_spell(name)


def create_spell(name: str, effect: str, dice: int, level: int, tags: str):
    spell = Spell(name, effect, dice, level, spliter(tags))
    return dl.create(spell)


def create_trait(name: str, effect: str, req: str, dice: int, is_passive: bool):
    trait = Trait(name, effect, spliter(req), dice, is_passive)
    return dl.create(trait)


def create_item(name: str, effect: str, cost: int, craft: int, tags: str, req: str = ""):
    item = Item(name, effect, cost, craft, spliter(tags), spliter(req))
    return dl.create(item)
