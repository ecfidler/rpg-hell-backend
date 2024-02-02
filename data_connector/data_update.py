import MySQLdb
from data_con_modules.data_con_create import add_item_tags, add_requirements, add_spell_tags
from data_con_modules.data_con_del import delete_core
from data_con_modules.data_con_read import read_one
from data_connector.data_delete import delete_creature
from data_connector.data_create import create, create_user
from data_con_modules.data_core import conn

from data_con_modules.data_con_update import update_trait_module

from models import Creature, Trait, Item, Spell, DBUser

from data_con_modules.data_core import get_db_config, do_query

#######################################################################
########################### Update Commands ###########################
#######################################################################

def update_trait_conn(name: str, trait: Trait):
    conn = MySQLdb.connect(**get_db_config())
    try:
        trait_id = read_one(f'SELECT id, name FROM objects WHERE name="{str(name).lower()}"',conn)[0]
        trait.id = trait_id

        do_query(f'UPDATE objects SET effect="{trait.effect}" WHERE id={trait_id}',conn)
        do_query(f'UPDATE traits SET dice={trait.dice}, is_passive={trait.is_passive} WHERE id={trait_id}',conn)

        delete_core(trait.id, "requirements",conn)
        add_requirements(trait, conn)

        conn.commit()
        data = {"id":trait.id}
    except Exception as e:
        data = {"Error": e}
        conn.rollback()
    conn.close()
    return data


def update_item_conn(name: str, item: Item):
    conn = MySQLdb.connect(**get_db_config())
    try:
        item_id = read_one(f'SELECT id, name FROM objects WHERE name="{str(name).lower()}"',conn)[0]
        item.id = item_id

        do_query(f'UPDATE objects SET effect="{item.effect}" WHERE id={item_id}',conn)
        do_query(f'UPDATE items SET cost={item.cost}, craft={item.craft} WHERE id={item_id}',conn)

        delete_core(item.id, "requirements",conn)
        add_requirements(item, conn)

        delete_core(item.id, "item_tags",conn)
        add_item_tags(item, conn)

        conn.commit()
        data = {"id":item.id}
    except Exception as e:
        data = {"Error": e}
        conn.rollback()
    conn.close()
    return data


def update_spell_conn(name: str, spell: Spell):
    conn = MySQLdb.connect(**get_db_config())
    try:
        spell_id = read_one(f'SELECT id, name FROM spells WHERE name="{str(name).lower()}"',conn)[0]
        spell.id = spell_id

        do_query(f'UPDATE spells SET effect="{spell.effect}", dice={spell.dice}, level={spell.level} WHERE id={spell_id}',conn)

        delete_core(spell.id, "spell_tags",conn)
        add_spell_tags(spell,conn)

        conn.commit()
        data = {"id":spell.id}
    except Exception as e:
        data = {"Error": e}
        conn.rollback()
    conn.close()
    return data


def update_creature(name: str, creature: Creature):
    id = delete_creature(name)["id"]
    return create(creature, id)

def update_creature(id: int, creature: Creature):
    delete_creature(id)
    return create(creature, id)


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
