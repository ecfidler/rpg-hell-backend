from models import Item, Trait, Spell
from data_con_modules.data_con_read import read_object

#######################################################################
########################### Update Commands ###########################
#######################################################################


def update_item(item, update_item: Item):
    cursor = conn.cursor()
    item_id = read_object(item)["id"]
    try:
        query = f"UPDATE objects SET name={update_item.name}, effect={update_item.effect} WHERE id={item_id}"
        cursor.execute(query)
        query = f"UPDATE items SET cost={update_item.craft}, craft={update_item.cost} WHERE id={item_id}"
        cursor.execute(query)
        # TODO: Somehow we need to do tags down here

        # TODO: Somehow we need to do requirements down here

        conn.commit()
        cursor.close()
    except:
        print("Update item error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def update_trait(trait, update_trait: Trait):
    cursor = conn.cursor()
    item_id = read_object(trait)["id"]
    try:
        query = f"UPDATE objects SET name={update_trait.name}, effect={update_trait.effect} WHERE id={item_id}"
        cursor.execute(query)
        query = f"UPDATE traits SET dice={update_trait.dice}, is_passive={update_trait.is_passive} WHERE id={item_id}"
        cursor.execute(query)
        # TODO: Somehow we need to do requirements down here

        conn.commit()
        cursor.close()
    except:
        print("Update trait error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}


def update_spell(spell, update_spell: Spell):
    cursor = conn.cursor()
    item_id = read_object(spell)["id"]
    try:
        query = f"UPDATE objects SET name={update_spell.name}, effect={update_spell.effect}, dice={update_spell.dice}, level={update_spell.level} WHERE id={item_id}"
        cursor.execute(query)
        # TODO: Somehow we need to do spell traits down here

        conn.commit()
        cursor.close()
    except:
        print("Update trait error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}

