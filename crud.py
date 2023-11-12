from models import Trait, Item, Spell
import data_connector as dl  # do_query, create, read_object, read_spell

# open query


def open_query(query: str):
    return dl.do_query(query)

# Objects


def get_object(id: int):
    return dl.read_object(id)


# todo: add other search params & support returning multiple results
def object_search(name: str):
    return dl.read_object(name)

# Items


def get_all_items():
    return dl.get_items()


def create_item(item: Item):
    # item = Item(name, effect, cost, craft, spliter(tags), spliter(req))
    return dl.create(item)


def update_item(id: int, new_item: Item):
    return dl.update_item(id, new_item)


def delete_item(id):
    return dl.delete_item(id)

# Traits


def create_trait(trait: Trait):
    return dl.create(trait)


def get_all_traits():
    return dl.get_traits()


def update_trait(id: int, new_trait: Trait):
    return dl.update_trait(int, new_trait)


def delete_trait(id: int):
    return dl.delete_trait(id)

# Spells


def get_spell(id: int):
    return dl.read_spell(id)


# todo: add other search params & support returning multiple results
def spell_search(name: str):
    return dl.read_spell(name)


def get_all_spells():
    return dl.get_spells()


def create_spell(spell: Spell):
    return dl.create(spell)


def update_spell(id: int, new_spell: Spell):
    return dl.update_spell(id, new_spell)


def delete_spell(id):
    return dl.delete_spell(id)
