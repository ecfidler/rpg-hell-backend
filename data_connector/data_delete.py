from data_con_modules.data_core import conn

from data_con_modules.data_con_del import delete_core

from data_connector.data_read import read_object, read_spell, read_user_from_discord_id, read_creature

#######################################################################
########################### Delete Commands ###########################
#######################################################################


def delete_item(item):
    item_id = read_object(item)["id"]
    cursor = conn.cursor()
    print(item_id)
    try:
        print("Del item tags")
        delete_core(item_id, "item_tags", cursor)

        print("Del item")
        delete_core(item_id, "items", cursor)
        print("Del requirements")
        delete_core(item_id, "requirements", cursor)
        print("Del object")
        delete_core(item_id, "objects", cursor)

        print(f"Deleated {item} from database")
        conn.commit()
        cursor.close()
    except:
        print("Del item error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def delete_trait(trait):
    item_id = read_object(trait)["id"]
    cursor = conn.cursor()
    try:
        print("Del traits")
        delete_core(item_id, "traits", cursor)
        print("Del requirements")
        delete_core(item_id, "requirements", cursor)
        print("Del object")
        delete_core(item_id, "objects", cursor)

        print(f"Deleated {trait} from database")

        conn.commit()
        cursor.close()
    except:
        print("Del item error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def delete_spell(spell):
    item_id = read_spell(spell)["id"]
    cursor = conn.cursor()
    try:
        print("Del spell tags")
        delete_core(item_id, "spell_tags", cursor)
        print("Del spell")
        delete_core(item_id, "spells", cursor)

        print(f"Deleated {spell} from database")
        conn.commit()
        cursor.close()
    except:
        print("Del spell error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def delete_user(user_id):
    item_id = read_user_from_discord_id(user_id)["id"]
    cursor = conn.cursor()
    try:
        print("Del user")
        delete_core(item_id, "users", cursor)

        print(f"Deleated {user_id} from database")
        conn.commit()
        cursor.close()
    except:
        print("Del user error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def delete_creature(creature):
    item_id = read_creature(creature)["id"]
    cursor = conn.cursor()
    try:
        print("Del creature types")
        delete_core(item_id, "creature_types", cursor)
        print("Del creature")
        delete_core(item_id, "creatures", cursor)

        print(f"Deleated {creature} from database")
        conn.commit()
        cursor.close()
    except:
        cursor.close()
        conn.rollback()
        raise Exception("Del creature error")
        

    return {"id": item_id}
