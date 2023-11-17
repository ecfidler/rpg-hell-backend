from models import Item, Trait, Spell

#######################################################################
########################## Creation Commands ##########################
#######################################################################


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


def create_obj(obj, cursor, _id: int = 0):  # item: Item
    query = f"INSERT INTO objects (name, effect) VALUES ({obj.name}, {obj.effect});"
    if _id:
        query = f"INSERT INTO objects (id, name, effect) VALUES ({_id}, {obj.name}, {obj.effect});"

    try:
        cursor.execute(query)
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        add_requirements(obj, cursor)
    except:
        print(query)
        Exception("Creation Obj Broke")
    return obj


# Route to create an item
# @app.post("/items/", response_model=Item)
def create_item(obj: Item, cursor, _id: int = 0):  # item: Item
    create_obj(obj, cursor, _id)
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


def create_trait(obj: Trait, cursor, _id: int = 0):  # item: Item
    create_obj(obj, cursor, _id)
    query = "INSERT INTO traits (id, dice, is_passive) VALUES (%s,%s,%s)"
    try:
        cursor.execute(query, (obj.id, obj.dice, obj.is_passive))
    except Exception as e:
        print(query)
        print(e)
        Exception()
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


def create_spell(obj, cursor, _id: int = 0):  # item: Item
    query = f"INSERT INTO spells (name, effect, dice, level) VALUES ({obj.name}, {obj.effect}, {obj.dice}, {obj.level});"
    if _id:
        query = f"INSERT INTO spells (id, name, effect, dice, level) VALUES ({_id},{obj.name}, {obj.effect}, {obj.dice}, {obj.level});"

    try:
        cursor.execute(query)
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        add_spell_tags(obj, cursor)
    except:
        print(query)
        Exception("Spell query Broke")
    return obj
