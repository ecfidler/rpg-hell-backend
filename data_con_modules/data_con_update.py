from data_con_modules.data_con_read import read_one
from data_con_modules.data_core import do_query
from data_connector.data_read import read_object
from models import Item, Trait, Spell

#######################################################################
########################### Update Commands ###########################
#######################################################################


def update_item(item, update_item: Item,conn):
    item_id = read_object(item)["id"]
    
    
    qItem = do_query(f"UPDATE objects SET name={update_item.name}, effect={update_item.effect} WHERE id={item_id}",conn)
    if qItem == -1: # check error
        return -1
    

    qItem = do_query(f"UPDATE items SET cost={update_item.craft}, craft={update_item.cost} WHERE id={item_id}",conn)
    if qItem == -1: # check error
        return -1

    # TODO: Somehow we need to do tags down here
    # TODO: Somehow we need to do requirements down here

    return {"id": item_id}


def update_trait_module(name:str , _update_trait: Trait, conn):
    trait_id = read_one(f'SELECT id, name FROM objects WHERE name="{str(name).lower()}"',conn)[0]
    _update_trait.id = trait_id

    do_query(f'UPDATE objects SET name="{_update_trait.name}", effect="{_update_trait.effect}" WHERE id={trait_id}',conn)
    do_query(f'UPDATE traits SET dice={_update_trait.dice}, is_passive={_update_trait.is_passive} WHERE id={trait_id}',conn)

    
    
    
    # TODO: Somehow we need to do requirements down here

    return {"id": trait_id}


def update_spell(spell, update_spell: Spell,conn):
    spell_id = read_object(spell)["id"]

    qItem = do_query(f"UPDATE objects SET name={update_spell.name}, effect={update_spell.effect}, dice={update_spell.dice}, level={update_spell.level} WHERE id={spell_id}",conn)
    if qItem == -1: # check error
        return -1
    
    # TODO: Somehow we need to do spell traits down here

    return {"id": spell_id}

