from models import Trait, Item, Spell
import data_connector as dl  # do_query, create, read_object, read_spell

# open query


def open_query(query: str):
    return dl.do_query(query)


def get_object(id: int):
    return dl.read_object(id)


# todo: add other search params & support returning multiple results
def object_search(name: str):
    return dl.read_object(name)


def get_all_traits():
    return dl.get_traits()


def get_all_items():
    return dl.get_items()


def get_spell(id: int):
    return dl.read_spell(id)


# todo: add other search params & support returning multiple results
def spell_search(name: str):
    return dl.read_spell(name)


def get_all_spells():
    return dl.get_spells()


def create_spell(spell: Spell):
    # spell = Spell(name, effect, dice, level, spliter(tags))
    return dl.create(spell)


def create_trait(trait: Trait):
    # trait = Trait(name, effect, spliter(req), dice, is_passive)
    return dl.create(trait)


def create_item(item: Item):
    # item = Item(name, effect, cost, craft, spliter(tags), spliter(req))
    return dl.create(item)
