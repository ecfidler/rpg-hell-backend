import MySQLdb
from fastapi import HTTPException

# Database configuration
db_config = {
    'host': 'shigure-djs',
    'user': 'ethan',
    'passwd': 'fidlerr',
    'db': 'rpghelltest1',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

#######################################################################
############################### Classes ###############################
#######################################################################

class Object():
    id: int = 0
    name : str
    effect : str = None
    req = []

    def __init__(self, _name: str, _effect: str, _req = []):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.req = _req

    def return_data(self):
        info = self.easy_data()
        self.update_info(info)
        return info
    
    def update_info(info):
        # this is a way to easily update other stuff
        pass
    

    def easy_data(self):
        return({"id": self.id, "name": self.name, "effect": self.effect,"req":self.req})
        

class Trait(Object):
    dice: int
    is_passive: bool = False
    
    def __init__(self, _name: str, _effect: str, _req, _dice: int, _is_passive = False):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.dice = int(_dice)
        self.is_passive = bool(_is_passive)
        if self.dice == 0:
            self.is_passive = True
        
        self.req = _req

    
    def update_info(self,info):
        info["dice"] = self.dice
        info["is_passive"] = self.is_passive
    

class Item(Object):
    cost: int = 0
    craft: int = 0
    tags = []
    
    def __init__(self, _name: str, _effect: str, _cost: int, _craft: int, _tags, _req=[]):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.cost = int(_cost)
        self.craft = int(_craft)
        self.tags = _tags

        self.req = _req

    def update_info(self,info):
        info["cost"] = self.cost
        info["craft"] = self.craft
        info["tags"] = self.tags
    

class Spell():
    id: int = 0
    name : str
    effect : str = None
    dice: int = 0
    level: int = 0
    tags = []
    
    def __init__(self, _name: str, _effect: str, _dice: int, _level: int, _tags):
        self.name = str(_name).lower()
        self.effect = str(_effect)
        self.dice = int(_dice)
        self.level = int(_level)
        self.tags = _tags

    def return_data(self):
        return {"id": self.id, "name": self.name, "effect": self.effect, "dice": self.dice, "level": self.level, "tags":self.tags}

def do_query(query):
    # todo: ef - fix the exceptions in here.
    cursor = conn.cursor()
    
    cursor.execute(query)
    item = cursor.fetchall()
    
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item not found with {err} lookup")

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
            create_obj(obj, cursor)
        elif clss == Item: # match (switch) cases dont exist in this vs of python. Very sad
            print("Creating Item")
            create_item(obj, cursor)
        elif clss == Trait:
            print("Creating Trait")
            create_trait(obj, cursor)
        elif clss == Spell:
            print("Creating Spell")
            create_spell(obj, cursor)
        else:
            Exception("it broke, no give item")
            
        cursor.close()
        conn.commit()
        print("Creation Successful")

    except:
        print(f"Error occured in {clss}")
        cursor.close()
        conn.rollback()
    

def add_requirements(obj,cursor):
    if obj.req != None and obj.req != []:
        query = "INSERT INTO requirements (object_id, type, value) VALUES "
        for rq in obj.req:
            if " " in rq:
                typ, val = rq.split(" ")
            else:
                typ = rq
                val = 1
            query += f'({obj.id}, "{str(typ).lower()}", {int(val)}),'
        query = query[:-1]+";" # required to do magic for later
        try:
            cursor.execute(query)
        except:
            print(query)
            Exception("Requirements query broke")
    
    return obj


def create_obj(obj, cursor): #item: Item
    query = "INSERT INTO objects (name, effect) VALUES (%s, %s);"
    try:
        cursor.execute(query, (obj.name, obj.effect))
        obj.id = cursor.lastrowid # needed in order to have an id for the next step
        add_requirements(obj,cursor)
    except:
        print(query)
        Exception("Creation Obj Broke")
    return obj


# Route to create an item
# @app.post("/items/", response_model=Item)
def create_item(obj: Item, cursor): #item: Item
    create_obj(obj,cursor)
    if obj.tags != None:
        query = "INSERT INTO items (id, cost, craft) VALUES (%s,%s,%s); INSERT INTO item_tags (item_id, name, value) VALUES "
        for tag in obj.tags:
            # print(tag)
            if "damage" in tag: # damage is backwards...
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
        query = query[:-1]+";" # required to do magic for later
        try:
            cursor.execute(query, (obj.id, obj.cost, obj.craft))
        except:
            print(query)
            Exception("Item query Broke")
        # print(query)
    return obj


def create_trait(obj: Trait, cursor): #item: Item
    create_obj(obj,cursor)
    query = "INSERT INTO traits (id, dice, is_passive) VALUES (%s,%s,%s)"
    try:
        cursor.execute(query, (obj.id, obj.dice, obj.is_passive))
    except:
        print(query)
        Exception("Trait query Broke")
    return obj



def add_spell_tags(obj: Spell, cursor): #item: Item
    if obj.tags != None:
        query = "INSERT INTO spell_tags (spell_id, name) VALUES "
        for tag in obj.tags:
            query += f'({obj.id}, "{str(tag).lower()}"),'
        query = query[:-1]+";" # required to do magic for later
        try:
            cursor.execute(query)
        except:
            print(query)
            Exception("Spell Tag query Broke")
        
    return obj


def create_spell(obj, cursor): #item: Item
    query = "INSERT INTO spells (name, effect, dice, level) VALUES (%s, %s, %s, %s);"
    try:
        cursor.execute(query, (obj.name, obj.effect, obj.dice, obj.level))
        obj.id = cursor.lastrowid # needed in order to have an id for the next step
        add_spell_tags(obj,cursor)
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
        #TODO: Somehow we need to do tags down here
        
        #TODO: Somehow we need to do requirements down here


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
        #TODO: Somehow we need to do requirements down here

    
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
        #TODO: Somehow we need to do spell traits down here

    
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
    
    

    info = {"id": item[0], "name": item[1], "effect": item[2],"req":req}
    
    # traits
    cursor.execute(f"SELECT dice, is_passive FROM traits WHERE id={info['id']}")
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

        cursor.execute(f"SELECT name, value FROM item_tags WHERE item_id={info['id']}")
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

    query = f"SELECT name FROM spell_tags WHERE spell_id={item[0]}"
    cursor.execute(query)
    tags = cleanup_tags(cursor.fetchall())
    
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item not found with {err} lookup")

    cursor.close()
    return {"id": item[0], "name": item[1], "effect": item[2], "dice": item[3], "level": item[4], "tags":tags}


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
        delete_core(item_id,"item_tags",cursor)
        
        print("Del item")
        delete_core(item_id,"items",cursor)
        print("Del requirements")
        delete_core(item_id,"requirements",cursor)
        print("Del object")
        delete_core(item_id,"objects",cursor)

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
        delete_core(item_id,"traits",cursor)
        print("Del requirements")
        delete_core(item_id,"requirements",cursor)
        print("Del object")
        delete_core(item_id,"objects",cursor)

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
        delete_core(item_id,"spell_tags",cursor)
        print("Del spell")
        delete_core(item_id,"spells",cursor)
        
        print(f"Deleated {spell} from database")
        conn.commit()
        cursor.close()
    except:
        print("Del spell error")
        cursor.close()
        conn.rollback()

    return {"id": item_id}




if __name__ == "__main__":
    pass
    # obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])
    # obj = Trait("Fishman","you become manfish", ["body 1","mind 1"], 0)
    # obj = Spell("poprocks","Boom Bam Bop", 2, 0,["ranged","attack"])
    # create(obj)

    # print(create_object(obj).id)

    # print(read_object(1))

    print(do_query("SELECT * FROM objects"))

    # print(read_spell(4))

    # cursor = conn.cursor()
    # query = "SELECT * FROM objects"
    # cursor.execute(query)
    # item = cursor.fetchall() # get all
    # cursor.close()
    # print(item)

    # print(delete_trait("Fishman"))