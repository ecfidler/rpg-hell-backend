from data_connector.data_delete import delete_trait, delete_item, delete_spell
from data_connector.data_create import create

from models import Trait, Item, Spell

#######################################################################
########################### Update Commands ###########################
#######################################################################


def update_trait(id: int, trait: Trait):
    delete_trait(id)
    return create(trait, id)


def update_item(id: int, item: Item):
    delete_item(id)
    return create(item, id)


def update_spell(id: int, spell: Spell):
    delete_spell(id)
    return create(spell, id)
