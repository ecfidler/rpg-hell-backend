from data_connector.data_delete import delete_trait, delete_item, delete_spell, delete_user
from data_connector.data_create import create, create_user
from data_con_modules.data_core import conn

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

def update_user(_id: int, user: DBUser):

    query = f'UPDATE users SET `name`="{user.username}", email="{user.email}" WHERE id={_id};'
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
        print(query)
        raise Exception("Update user Broke")
    return user

    # delete_user(user.discord_id)
    # return create_user(user, id)