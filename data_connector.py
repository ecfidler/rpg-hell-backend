
import json
import MySQLdb
from fastapi import HTTPException, Query


from models import Object, Item, Trait, Spell

from data_con_modules.data_con_create import create_obj, create_item, create_trait, create_spell
# from data_con_modules.data_con_update import update_item, update_spell, update_trait
from data_con_modules.data_con_del import delete_core
from data_con_modules.data_con_read import cleanup_tags, cleanup_search, cleanup_tags_req
from data_con_modules.data_con_filter import cleanup_filter, get_filter_query

# Database configuration
with open('db_config.json') as json_file:
    db_config = json.load(json_file)


# Create a connection to the database
conn = MySQLdb.connect(**db_config)


#######################################################################
############################## Mysc Tools #############################
#######################################################################


def spliter(data):
    lst = str(data).lower().split(", ")
    return (lst)


def do_query(query):
    # todo: ef - fix the exceptions in here.
    cursor = conn.cursor()

    cursor.execute(query)
    item = cursor.fetchall()

    # # This isn't really needed, it can just return nothing in response to the query
    # if item is None:
    #     cursor.close()
    #     raise ValueError(
    #         status_code=404, detail=f"Item(s) not found with query: \"{query}\"")

    cursor.close()
    return item

#######################################################################
########################## Creation Commands ##########################
#######################################################################


def create(obj, _id:int = None):
    cursor = conn.cursor()
    print("Start Creation")

    try:
        clss = obj.__class__
        
        if clss == Object:
            print("Creating Obj")
            obj = create_obj(obj, cursor, _id)
        # match (switch) cases dont work for objects aparently
        elif clss == Item:
            print("Creating Item")
            obj = create_item(obj, cursor, _id)
        elif clss == Trait:
            print("Creating Trait")
            obj = create_trait(obj, cursor, _id)
        elif clss == Spell:
            print("Creating Spell")
            obj = create_spell(obj, cursor, _id)
        else:
            raise TypeError("it broke, no give item")

        cursor.close()
        conn.commit()
        print("Creation Successful")
        return obj.id

    except:
        print(f"Error occured in {clss}")
        cursor.close()
        conn.rollback()
        return -1


#######################################################################
########################### Update Commands ###########################
#######################################################################


def update_trait(id:int, trait: Trait):
    delete_trait(id)
    return create(trait,id)


def update_item(id:int, item: Item):
    delete_item(id)
    return create(item,id)


def update_trait(id:int, spell: Spell):
    delete_spell(id)
    return create(spell,id)

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

    cursor.execute(query)
    item = cursor.fetchone()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    query = f"SELECT type, value FROM requirements WHERE object_id={item[0]}"
    cursor.execute(query)
    req = cleanup_tags(cursor.fetchall())

    info = {"id": item[0], "name": item[1], "effect": item[2], "req": req}

    # traits
    cursor.execute(
        f"SELECT dice, is_passive FROM traits WHERE id={info['id']}")
    item = cursor.fetchone()
    if item != None:
        info["dice"] = item[0]
        info["is_passive"] = item[1]

    # items
    cursor.execute(f"SELECT cost, craft FROM items WHERE id={info['id']}")
    item = cursor.fetchone()
    if item != None:
        info["cost"] = item[0]
        info["craft"] = item[1]

        cursor.execute(
            f"SELECT name, value FROM item_tags WHERE item_id={info['id']}")
        tags = cleanup_tags(cursor.fetchall())
        info["tags"] = tags

    cursor.close()
    return info


def read_spell(spell_quiry):
    cursor = conn.cursor()
    try:
        err = "ID"
        query = f"SELECT id, name, effect, dice, level FROM spells WHERE id={int(spell_quiry)}"
    except:
        err = "NAME"
        query = f'SELECT id, name, effect, dice, level FROM spells WHERE name="{str(spell_quiry).lower()}"'

    cursor.execute(query)
    item = cursor.fetchone()

    if item is None:
        raise HTTPException(
            status_code=404, detail=f"Item not found with {err} lookup")

    query = f"SELECT name FROM spell_tags WHERE spell_id={item[0]}"
    cursor.execute(query)
    tags = cleanup_tags(cursor.fetchall())

    cursor.close()
    return {"id": item[0], "name": item[1], "effect": item[2], "dice": item[3], "level": item[4], "tags": tags}



def get_traits(_ids:list[int]=[]):
    """
    Returns all traits
    """
    cursor = conn.cursor()

    if len(_ids):
        query = f"SELECT objects.id, objects.name, objects.effect, traits.dice, traits.is_passive FROM objects, traits WHERE objects.id=traits.id AND objects.id IN ({str(_ids)[1:-1]});"
    else:
        query = f"SELECT objects.id, objects.name, objects.effect, traits.dice, traits.is_passive FROM objects INNER JOIN traits ON objects.id=traits.id;"
    cursor.execute(query)
    traits, ids = cleanup_search(cursor.fetchall())

    # remove the [] from ids
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_req(traits, cursor.fetchall(),"req")

    cursor.close()
    return traits, ids


def get_items(_ids:list[int]=[]):
    """
    Returns all items
    """
    cursor = conn.cursor()

    if len(_ids):
        query = f"SELECT objects.id, objects.name, objects.effect, items.cost, items.craft FROM objects, items WHERE objects.id=items.id AND objects.id IN ({str(_ids)[1:-1]});"
    else:
        query = f"SELECT objects.id, objects.name, objects.effect, items.cost, items.craft FROM objects INNER JOIN items ON objects.id=items.id;"
    
    # print(query)
    cursor.execute(query)
    items, ids = cleanup_search(cursor.fetchall(),"items")

    # remove the []
    query = f"SELECT item_id, name, value FROM item_tags WHERE item_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_req(items, cursor.fetchall(),'tags')

    # remove the []
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    tmpitm = cursor.fetchall() # items may not have requirements
    if len(tmpitm):
        cleanup_tags_req(items, tmpitm, 'req')

    cursor.close()
    return items, ids


def get_spells(_ids:list[int]=[]):
    """
    Returns all spells
    """
    cursor = conn.cursor()

    if len(_ids):
        query = f"SELECT id, name, effect, dice, level FROM spells WHERE id IN ({str(_ids)[1:-1]});"
    else:
        query = f"SELECT id, name, effect, dice, level FROM spells;"


    cursor.execute(query)
    spells, ids = cleanup_search(cursor.fetchall(),"spells")

    # remove the []
    query = f"SELECT spell_id, name FROM spell_tags WHERE spell_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    # print(cursor.fetchall())
    cleanup_tags_req(spells, cursor.fetchall(),'tags')

    cursor.close()
    return spells, ids

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


#######################################################################
########################### Filter Commands ###########################
#######################################################################



def filter_base(loc: str, reqs: list[str]=[],tags: list[str]=[]):
    # SELECT DISTINCT id, name FROM objects WHERE id IN 
    # (SELECT object_id FROM requirements WHERE 
    # object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("Body") AND `value` IN (2))
    # AND object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("mind") AND `value` IN (1))
    # )

    cursor = conn.cursor()
    
    query = get_filter_query(loc,reqs,tags)

    print(query)
    cursor.execute(query)
    ids = cleanup_filter(cursor.fetchall())

    cursor.close()
    return ids


def filter_traits_by_reqs(reqs:list[str]):
    ids = filter_base("traits",reqs)
    if len(ids):
        data, ids = get_traits(ids)
    else:
        return [],[]
    
    return data, ids

def filter_items_by_reqs(reqs:list[str]):
    ids = filter_base("items",reqs)
    if len(ids):
        data, ids = get_items(ids)
    else:
        return [],[]
    
    return data, ids

def filter_items_by_tags(tags:list[str]):
    ids = filter_base("items",[],tags)
    if len(ids):
        data, ids = get_items(ids)
    else:
        return [],[]

    return data, ids

def filter_spells_by_tags(tags:list[str]):
    ids = filter_base("spells",[],tags)
    if len(ids):
        data, ids = get_spells(ids)
    else:
        return [],[]

    return data, ids




if __name__ == "__main__":
    pass
    # obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])
    # obj = Trait("Fishman","you become manfish", ["body 1","mind 1"], 0)
    # obj = Spell("poprocks","Boom Bam Bop", 2, 0,["ranged","attack"])
    # create(obj)

    # print(create_object(obj).id)

    # print(read_object(1))

    # print(read_spell("poprocks"))
    # print(get_items())
    # print(get_traits())
    # print(get_spells([1]))
    
    
    # print(filter_base("spells",[],["touch"])) # Fails if given both at the same time but works seprately
    # print(filter_spells_by_tags(["touch","utility"]))
    # print(filter_traits_by_reqs(["soul 2","body 1"]))
    # print(filter_items_by_reqs(["body 2"]))
    # print(filter_items_by_tags(["tiny",'potion']))


    # ids = [477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629]

    # [{1,stuff},{3,stuff},{63,stuff}]
    # [[(1,name,val),(1,name,val)], [], [(63,name,val)],]

    # txt = ""
    # for a in ids:
    #     txt += f"({a}),"

    # print(txt)

    # print(read_spell(4))

    # cursor = conn.cursor()
    # query = "SELECT * FROM objects"
    # cursor.execute(query)
    # item = cursor.fetchall() # get all
    # cursor.close()
    # print(item)

    # print(delete_trait("Fishman"))
