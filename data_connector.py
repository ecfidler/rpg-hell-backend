
import json
import MySQLdb
from fastapi import HTTPException

from models import Object, Item, Trait, Spell

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


def create(obj):
    cursor = conn.cursor()
    print("Start Creation")
    try:
        clss = obj.__class__
        if clss == Object:
            print("Creating Obj")
            obj = create_obj(obj, cursor)
        # match (switch) cases dont exist in this vs of python. Very sad
        elif clss == Item:
            print("Creating Item")
            obj = create_item(obj, cursor)
        elif clss == Trait:
            print("Creating Trait")
            obj = create_trait(obj, cursor)
        elif clss == Spell:
            print("Creating Spell")
            obj = create_spell(obj, cursor)
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


def add_requirements(obj, cursor):
    if obj.req != None and obj.req != []:
        query = "INSERT INTO requirements (object_id, type, value) VALUES "
        for rq in obj.req:
            if " " in rq:
                typ, val = rq.split(" ")
            else:
                typ = rq
                val = 1
            query += f'({obj.id}, "{str(typ).lower()}", {int(val)}),'
        query = query[:-1]+";"  # required to do magic for later
        try:
            cursor.execute(query)
        except:
            print(query)
            Exception("Requirements query broke")

    return obj


def create_obj(obj, cursor):  # item: Item
    query = "INSERT INTO objects (name, effect) VALUES (%s, %s);"
    try:
        cursor.execute(query, (obj.name, obj.effect))
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        add_requirements(obj, cursor)
    except:
        print(query)
        Exception("Creation Obj Broke")
    return obj


# Route to create an item
# @app.post("/items/", response_model=Item)
def create_item(obj: Item, cursor):  # item: Item
    create_obj(obj, cursor)
    if obj.tags != None:
        query = "INSERT INTO items (id, cost, craft) VALUES (%s,%s,%s); INSERT INTO item_tags (item_id, name, value) VALUES "
        for tag in obj.tags:
            # print(tag)
            if "damage" in tag:  # damage is backwards...
                val, typ = tag.split(" ")
            elif " " in tag:
                t = tag.split(" ")
                # print(t)
                try:
                    typ, val = " ".join(t[:-1]), int(t[-1])
                except:
                    typ = tag
                    val = 0
                # print(typ)

            else:
                typ = tag
                val = 0

            query += f'({obj.id}, "{str(typ).lower()}", {int(val)}),'
        query = query[:-1]+";"  # required to do magic for later
        try:
            cursor.execute(query, (obj.id, obj.cost, obj.craft))
        except:
            print(query)
            Exception("Item query Broke")
        # print(query)
    return obj


def create_trait(obj: Trait, cursor):  # item: Item
    create_obj(obj, cursor)
    query = "INSERT INTO traits (id, dice, is_passive) VALUES (%s,%s,%s)"
    try:
        cursor.execute(query, (obj.id, obj.dice, obj.is_passive))
    except:
        print(query)
        Exception("Trait query Broke")
    return obj


def add_spell_tags(obj: Spell, cursor):  # item: Item
    if obj.tags != None:
        query = "INSERT INTO spell_tags (spell_id, name) VALUES "
        for tag in obj.tags:
            query += f'({obj.id}, "{str(tag).lower()}"),'
        query = query[:-1]+";"  # required to do magic for later
        try:
            cursor.execute(query)
        except:
            print(query)
            Exception("Spell Tag query Broke")

    return obj


def create_spell(obj, cursor):  # item: Item
    query = "INSERT INTO spells (name, effect, dice, level) VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(query, (obj.name, obj.effect, obj.dice, obj.level))
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        add_spell_tags(obj, cursor)
    except:
        print(query)
        Exception("Spell query Broke")
    return obj

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


#######################################################################
############################ Read Commands ############################
#######################################################################

def cleanup_tags(tags):
    t = []
    for tag in tags:
        if len(tag) == 2:
            t.append(f"{tag[0]} {tag[1]}")
        else:
            t.append(str(tag[0]))
    return t


def cleanup_req_large(traits, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            t.append((tag[1], tag[2]))
        else:
            traits[loc]["req"] = cleanup_tags(t)
            loc += 1
            t = [(tag[1], tag[2])]
            _id = tag[0]

    traits[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return traits


def cleanup_item_req_large(items, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            t.append((tag[1], tag[2]))
        else:
            while items[loc]["id"] != _id:
                loc += 1
            items[loc]["req"] = cleanup_tags(t)
            loc += 1
            t = [(tag[1], tag[2])]
            _id = tag[0]

    while items[loc]["id"] != _id:
        loc += 1
    items[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return items


def cleanup_tags_large(items, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            try:
                t.append((tag[1], tag[2]))
            except:
                t.append((tag[1],))
        else:
            items[loc]["tags"] = cleanup_tags(t)
            loc += 1
            try:
                t = [(tag[1], tag[2])]
            except:
                t = [(tag[1],)]
            # t = [(tag[1], tag[2])]
            _id = tag[0]

    items[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return items


def cleanup_search_traits(items):
    data, ids = [], []
    for item in items:
        info = {"id": item[0], "name": item[1], "effect": item[2],
                "dice": item[3], "is_passive": item[4]}
        data.append(info)
        ids.append(item[0])
    return data, ids


def cleanup_search_items(items):
    data, ids = [], []
    for item in items:
        info = {"id": item[0], "name": item[1],
                "effect": item[2], "cost": item[3], "craft": item[4]}
        data.append(info)
        ids.append(item[0])
    return data, ids


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


def get_traits():
    """
    Returns all traits
    """
    cursor = conn.cursor()

    query = f"SELECT objects.id, objects.name, objects.effect, traits.dice, traits.is_passive FROM objects INNER JOIN traits ON objects.id=traits.id;"
    cursor.execute(query)
    traits, ids = cleanup_search_traits(cursor.fetchall())

    # remove the [] from ids
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_req_large(traits, cursor.fetchall())

    cursor.close()
    return traits, ids


def get_items():
    """
    Returns all items
    """
    cursor = conn.cursor()

    query = f"SELECT objects.id, objects.name, objects.effect, items.cost, items.craft FROM objects INNER JOIN items ON objects.id=items.id;"
    cursor.execute(query)
    items, ids = cleanup_search_items(cursor.fetchall())

    # remove the []
    query = f"SELECT item_id, name, value FROM item_tags WHERE item_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_large(items, cursor.fetchall())

    # remove the []
    query = f"SELECT object_id, type, value FROM requirements WHERE object_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_item_req_large(items, cursor.fetchall())

    cursor.close()
    return items, ids


def get_spells():
    """
    Returns all spells
    """
    cursor = conn.cursor()

    query = f"SELECT id, name, effect, dice, level FROM spells;"
    cursor.execute(query)
    spells, ids = cleanup_search_items(cursor.fetchall())

    # remove the []
    query = f"SELECT spell_id, name FROM spell_tags WHERE spell_id IN ({str(ids)[1:-1]})"
    cursor.execute(query)
    cleanup_tags_large(spells, cursor.fetchall())

    cursor.close()
    return spells, ids

#######################################################################
########################### Delete Commands ###########################
#######################################################################


def delete_core(id: int, loc: str, cursor):
    id_types = {"spells": "id",
                "spell_tags": "spell_id",
                "traits": "id",
                "objects": "id",
                "item_tags": "item_id",
                "items": "id",
                "requirements": "object_id"}

    query = f"DELETE FROM {loc} WHERE {id_types[loc]}={id}"
    # print(query)
    cursor.execute(query)


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


def cleanup_filter(items):
    ids = []
    for item in items:
        ids.append(item[0])
    return ids


def filter_base(loc: str, reqs: list[str]=[],tags: list[str]=[]):
    # SELECT DISTINCT id, name FROM objects WHERE id IN 
    # (SELECT object_id FROM requirements WHERE 
    # object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("Body") AND `value` IN (2))
    # AND object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("mind") AND `value` IN (1))
    # )

    cursor = conn.cursor()

    places = {"objects": "objects",
              "traits": "objects",
              "items": "objects",
              "spells": "spells"}
    place_tags = {"items": ["item_tags","item_id"], "spells": ["spell_tags","spell_id"]}

    query = f"SELECT DISTINCT id FROM {places[loc]} WHERE id IN ("
    if len(reqs): # check for items in req
        query += "(SELECT object_id FROM requirements WHERE "
        first = True
        for req in reqs:
            name, val = req.split(" ")

            if not first:
                query += "AND "
            else:
                first = False

            query += f'object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("{name}") AND `value` IN ({val})) '
        
        query = query[:-1]+") " # lop off extra space and add end
    
    if len(tags): # check for items in req
        if len(reqs): # this does not work... sql bullll
            query += "AND "

        query += f"(SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE "
        first = True
        for tag in tags:
            if not first:
                query += "AND "
            else:
                first = False

            try:
                name, val = tag.split(" ")
                query += f'{place_tags[loc][1]} IN (SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE `name` IN ("{name}") AND `value` IN ({val})) '
        
            except: # for spells
                query += f'{place_tags[loc][1]} IN (SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE `name` IN ("{tag}")) '
            
        query = query[:-1]+") " # lop off extra space and add end
    


    query = query[:-1]+")"
    

    

    # print(query)
    cursor.execute(query)
    ids = cleanup_filter(cursor.fetchall())

    cursor.close()
    return ids


if __name__ == "__main__":
    pass
    # obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])
    # obj = Trait("Fishman","you become manfish", ["body 1","mind 1"], 0)
    # obj = Spell("poprocks","Boom Bam Bop", 2, 0,["ranged","attack"])
    # create(obj)

    # print(create_object(obj).id)

    # print(read_object(1))

    # print(read_spell("pop rocks"))
    # print(get_items())
    print(filter_base("spells",[],["touch"])) # Fails if given both at the same time but works seprately

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
