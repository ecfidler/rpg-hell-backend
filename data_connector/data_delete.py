import MySQLdb
from data_con_modules.data_con_del import delete_core

from data_connector.data_read import read_object, read_spell, read_user_from_discord_id, read_creature

from data_con_modules.data_core import get_db_config
#######################################################################
########################### Delete Commands ###########################
#######################################################################


def delete_item(item):
    item_id = read_object(item)["id"]

    conn = MySQLdb.connect(**get_db_config())
    
    print("Del item tags")
    delete_core(item_id, "item_tags", conn)

    print("Del item")
    delete_core(item_id, "items",conn)

    print("Del requirements")
    delete_core(item_id, "requirements",conn)
    
    print("Del object")
    delete_core(item_id, "objects", conn)

    print(f"Deleated {item} from database")

    conn.close()
    
    return {"id": item_id}


def delete_trait_conn(trait_id):
    conn = MySQLdb.connect(**get_db_config())

    try:
        print("Del traits")
        delete_core(trait_id, "traits",conn)
        
        print("Del requirements")
        delete_core(trait_id, "requirements",conn)
        
        print("Del object")
        delete_core(trait_id, "objects",conn)

        print(f"Deleated {trait_id} from database")
        data = {"id": trait_id}

        conn.commit()
    except Exception as e:
        conn.rollback()
        data = {"Error":e}

    conn.close()

    return data


def delete_spell(spell):
    item_id = read_spell(spell)["id"]

    conn = MySQLdb.connect(**get_db_config())

    print("Del spell tags")
    delete_core(item_id, "spell_tags",conn)
    
    print("Del spell")
    delete_core(item_id, "spells",conn)

    print(f"Deleated {spell} from database")

    conn.close()
    return {"id": item_id}


def delete_user(user_id):
    item_id = read_user_from_discord_id(user_id)["id"]

    conn = MySQLdb.connect(**get_db_config())
    
    print("Del user")
    dl = delete_core(item_id, "users",conn)

    print(f"Deleated {user_id} from database")

    conn.close()

    return {"id": item_id}


def delete_creature(creature):
    item_id = read_creature(creature)["id"]

    conn = MySQLdb.connect(**get_db_config())
    
    print("Del creature types")
    delete_core(item_id, "creature_types",conn)
    print("Del creature")
    delete_core(item_id, "creatures",conn)
        
    print(f"Deleated {creature} from database")
    conn.close()
    return {"id": item_id}
