import MySQLdb
from data_con_modules.data_con_del import delete_core

from data_connector.data_read import read_object, read_spell, read_user_from_discord_id, read_creature

from data_con_modules.data_core import db_config
#######################################################################
########################### Delete Commands ###########################
#######################################################################


def delete_item(item):
    item_id = read_object(item)["id"]

    conn = MySQLdb.connect(**db_config)
    
    print("Del item tags")
    dl = delete_core(item_id, "item_tags", conn)
    if dl == -1:
        return -1

    print("Del item")
    delete_core(item_id, "items",conn)
    if dl == -1:
        return -1

    print("Del requirements")
    delete_core(item_id, "requirements",conn)
    if dl == -1:
        return -1
    
    print("Del object")
    delete_core(item_id, "objects")
    if dl == -1:
        return -1

    print(f"Deleated {item} from database")
    
    return {"id": item_id}


def delete_trait(trait):
    item_id = read_object(trait)["id"]


    print("Del traits")
    dl = delete_core(item_id, "traits")
    if dl == -1:
        return -1
    
    print("Del requirements")
    delete_core(item_id, "requirements")
    if dl == -1:
        return -1
    
    print("Del object")
    delete_core(item_id, "objects")
    if dl == -1:
        return -1

    print(f"Deleated {trait} from database")

    return {"id": item_id}


def delete_spell(spell):
    item_id = read_spell(spell)["id"]

    print("Del spell tags")
    dl = delete_core(item_id, "spell_tags")
    if dl == -1:
        return -1
    
    print("Del spell")
    dl = delete_core(item_id, "spells")
    if dl == -1:
        return -1

    print(f"Deleated {spell} from database")
    return {"id": item_id}


def delete_user(user_id):
    item_id = read_user_from_discord_id(user_id)["id"]
    
    print("Del user")
    dl = delete_core(item_id, "users")
    if dl == -1:
        return -1
    print(f"Deleated {user_id} from database")

    return {"id": item_id}


def delete_creature(creature):
    item_id = read_creature(creature)["id"]
    
    print("Del creature types")
    dl = delete_core(item_id, "creature_types")
    print("Del creature")
    dl = delete_core(item_id, "creatures")

    if dl == -1:
        raise Exception("Del creature error")
        
    print(f"Deleated {creature} from database")
    return {"id": item_id}
