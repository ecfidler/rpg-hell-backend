from data_connector.data_delete import delete_trait, delete_item, delete_spell, delete_user
from data_connector.data_create import create, create_user

from models import Trait, Item, Spell, DBUser

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

def update_user(id: int, user: DBUser):
    delete_user(user.discord_id)
    return create_user(user, id)