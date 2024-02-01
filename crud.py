from logging import Filter
from fastapi import HTTPException
from models import Creature, Trait, Item, Spell, DBUser
# import data_connector as dl  # do_query, create, read_object, read_spell
import data_connector.data_create as create
import data_connector.data_read as read
import data_connector.data_update as update
import data_connector.data_delete as delete
import data_connector.data_filter as filter
# import data_connector.data_filter as filter

from enumeration import FilterOption


from data_con_modules.data_core import do_query

# open query


def open_query(query: str):
    return do_query(query)

# Objects


def get_object(id: int):
    return read.read_object(id)


# todo: add other search params & support returning multiple results
def object_search(name: str):
    return read.read_object(name)

# Items


def get_all_items_crud():
    items, ids = read.get_items_conn()
    return dict(zip(ids, items))


def create_item_crud(item: Item):
    # item = Item(name, effect, cost, craft, spliter(tags), spliter(req))
    return create.create(item)


def update_item_crud(id: int, new_item: Item):
    return update.update_item_conn(id, new_item)


def delete_item_crud(id):
    return delete.delete_item_conn(id)


def filter_item(filters: str, option: FilterOption):
    _filters = filters.split(',')
    if (option == FilterOption.requirements):
        data, ids = filter.filter_items_by_reqs(_filters)
    elif (option == FilterOption.tags):
        data, ids = filter.filter_items_by_tags(_filters)
    else:
        raise ValueError(
            "Query 'filter' is of Enum type FilterOption which has tags = 1 & requirements = 2")
    return dict(zip(ids, data))

# Traits


def create_trait_crud(trait: Trait):
    return create.create(trait)


def get_all_traits():
    traits, ids = read.get_traits_conn()
    return dict(zip(ids, traits))


def update_trait_crud(name: str, new_trait: Trait):
    return update.update_trait_conn(name, new_trait)


def delete_trait_crud(id: int):
    data = delete.delete_trait_conn(id)
    return data


def filter_trait(requirements: str):
    _requirements = requirements.split(',')
    data, ids = filter.filter_traits_by_reqs(_requirements)
    return dict(zip(ids, data))

# Spells


def get_spell_crud(id: int):
    return read.read_spell_conn(id)


# todo: add other search params & support returning multiple results
def spell_search_crud(name: str):
    return read.read_spell_conn(name)


def get_all_spells_crud():
    spells, ids = read.get_spells_conn()
    return dict(zip(ids, spells))


def create_spell_crud(spell: Spell):
    return create.create(spell)


def update_spell_crud(id: int, new_spell: Spell):
    return update.update_spell_conn(id, new_spell)


def spell_delete_crud(id):
    return delete.delete_spell_conn(id)


def filter_spell_crud(tags: str):
    _tags = tags.split(',')
    data, ids = filter.filter_spells_by_tags_conn(_tags)
    return dict(zip(ids, data))

# Users


def get_create_user(user: DBUser):
    try:
        res = get_user(user.discord_id)

        if not user.compare(res):
            user.id = res["id"]
            res = update_user(user)

    except:
        res = create_user(user)

    return res


def get_user(discord_id: int):
    return read.read_user_from_discord_id(discord_id)


def create_user(user: DBUser):
    return create.create_user(user)


def update_user(user: DBUser):
    return update.update_user(user.id, user)


# creatures

def create_creature(creature: Creature):
    return create.create(creature)


def get_creature(id: int):
    return read.read_creature(id)


def creature_search(name: str):
    return read.read_creature(name)


def delete_creature(id: int):
    return delete.delete_creature(id)


def update_creature(id: int, new_creature: Creature):
    return update.update_creature(id, new_creature)
