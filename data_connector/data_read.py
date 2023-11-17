from data_con_modules.data_core import conn

from data_con_modules.data_con_read import read_one, read_list, cleanup_search, cleanup_tags_req
from fastapi import HTTPException

#######################################################################
############################ Read Commands ############################
#######################################################################


def read_object(object_id):
    cursor = conn.cursor()
    try:
        err = "ID"
        query = f"SELECT id, name, effect FROM objects WHERE id={int(object_id)}"
    except:
        err = "NAME"
        query = f'SELECT id, name, effect FROM objects WHERE name="{str(object_id).lower()}"'

    item = read_one(query,cursor)

    query = f"SELECT type, value FROM requirements WHERE object_id={item[0]}"
    req = read_list(query, cursor, ignore_missing=True)

    info = {"id": item[0], "name": item[1], "effect": item[2], "req": req}

    # traits
    query = f"SELECT dice, is_passive FROM traits WHERE id={info['id']}"
    trait_data = read_one(query,cursor, ignore_missing=True)
    if trait_data != None:
        info["dice"] = trait_data[0]
        info["is_passive"] = trait_data[1]

    # items
    cursor.execute(f"SELECT cost, craft FROM items WHERE id={info['id']}")
    item_data = read_one(query,cursor, ignore_missing=True)
    if item_data != None:
        info["cost"] = item_data[0]
        info["craft"] = item_data[1]

        query = f"SELECT name, value FROM item_tags WHERE item_id={info['id']}"
        tags = read_list(query,cursor)
        info["tags"] = tags

    cursor.close()
    return info


def read_spell(spell_quiry):
    cursor = conn.cursor()
    try:
        query = f"SELECT id, name, effect, dice, level FROM spells WHERE id={int(spell_quiry)}"
    except:
        query = f'SELECT id, name, effect, dice, level FROM spells WHERE name="{str(spell_quiry).lower()}"'

    spell = read_one(query,cursor)

    query = f"SELECT name FROM spell_tags WHERE spell_id={spell[0]}"
    tags = read_list(query,cursor)

    cursor.close()
    return {"id": spell[0], "name": spell[1], "effect": spell[2], "dice": spell[3], "level": spell[4], "tags": tags}


def get_traits(_ids: list[int] = []):
    """
    Returns all traits
    """
    cursor = conn.cursor()
    query = f"SELECT objects.id, objects.name, objects.effect, traits.dice, traits.is_passive FROM objects INNER JOIN traits ON objects.id=traits.id"
    
    if len(_ids):
        query += f" AND objects.id IN ({str(_ids)[1:-1]});"
    
    cursor.execute(query)
    traits, ids = cleanup_search(cursor.fetchall())

    # remove the [] from ids
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_req(traits, cursor.fetchall(), "req")

    cursor.close()
    return traits, ids


def get_items(_ids: list[int] = []):
    """
    Returns all items
    """
    cursor = conn.cursor()
    query = f"SELECT objects.id, objects.name, objects.effect, items.cost, items.craft FROM objects, items WHERE objects.id=items.id"
        
    if len(_ids):
        query += f" AND objects.id IN ({str(_ids)[1:-1]})"
    
    # print(query)
    cursor.execute(query)
    items, ids = cleanup_search(cursor.fetchall(), "items")

    # remove the []
    query = f"SELECT item_id, name, value FROM item_tags WHERE item_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_req(items, cursor.fetchall(), 'tags')

    # remove the []
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    tmpitm = cursor.fetchall()  # items may not have requirements
    if len(tmpitm):
        cleanup_tags_req(items, tmpitm, 'req')

    cursor.close()
    return items, ids


def get_spells(_ids: list[int] = []):
    """
    Returns all spells
    """
    cursor = conn.cursor()

    query = f"SELECT id, name, effect, dice, level FROM spells"

    if len(_ids):
        query += f" WHERE id IN ({str(_ids)[1:-1]});"

    cursor.execute(query)
    spells, ids = cleanup_search(cursor.fetchall(), "spells")

    # remove the []
    query = f"SELECT spell_id, name FROM spell_tags WHERE spell_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    # print(cursor.fetchall())
    cleanup_tags_req(spells, cursor.fetchall(), 'tags')

    cursor.close()
    return spells, ids


def read_user_from_name(user_name):
    cursor = conn.cursor()
    query = f'SELECT discord_id, name, is_admin FROM users WHERE name="{str(user_name).lower()}"'

    cursor.execute(query)
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    cursor.close()
    return user


def read_user_from_discord_id(discord_id):
    cursor = conn.cursor()
    query = f'SELECT discord_id, name, is_admin FROM users WHERE discord_id="{str(discord_id).lower()}"'

    cursor.execute(query)
    user = cursor.fetchone()

    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    cursor.close()
    return user


def get_users(_ids: list[int] = []):
    cursor = conn.cursor()
    query = f"SELECT id, discord_id, name, is_admin FROM users"

    if len(_ids):
        query += f" WHERE id IN ({str(_ids)[1:-1]});"
    
    try:
        cursor.execute(query)
        users, ids = cleanup_search(cursor.fetchall(), "spells")
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
        print(query)
        raise Exception("get users Broke")
    return users, ids


