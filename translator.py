import MySQLdb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'B',
    'passwd': 'hell',
    'db': 'rpghelldata',
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)
app = FastAPI()


class Object():
    id: int
    name : str
    effect : str = None
    req = []

    def __init__(self, _name: str, _effect: str, _req = []):
        self.name = _name
        self.effect = _effect
        self.req = _req
        

class Trait(Object):
    dice: int
    is_passive: bool = False
    
    def __init__(self, _name: str, _effect: str, _req, _dice: int, _is_passive = False):
        self.name = _name
        self.effect = _effect
        self.dice = _dice
        self.is_passive = _is_passive
        if self.dice == 0:
            self.is_passive = True
        
        self.req = _req


class Item(Object):
    cost: int = 0
    craft: int = 0
    tags = []
    
    def __init__(self, _name: str, _effect: str, _cost: int, _craft: int, _tags, _req=[]):
        self.name = _name
        self.effect = _effect
        self.cost = _cost
        self.craft = _craft
        self.tags = _tags

        self.req = _req
    

class Spell():
    id: int
    name : str
    effect : str = None
    dice: int = 0
    level: int = 0
    tags = []
    
    def __init__(self, _name: str, _effect: str, _dice: int, _level: int, _tags):
        self.name = _name
        self.effect = _effect
        self.dice = _dice
        self.level = _level
        self.tags = _tags


def create(obj):
    cursor = conn.cursor()
    try:
        clss = obj.__class__
        if clss == Object:
            create_obj(obj, cursor)
        elif clss == Item: # match (switch) cases dont exist in this vs of python. Very sad
            create_item(obj, cursor)
        elif clss == Trait:
            create_trait(obj, cursor)
        elif clss == Spell:
            create_spell(obj, cursor)
            
        cursor.close()
        conn.commit()
    except:
        print("Error occured")
        cursor.close()
        conn.rollback()

def add_requirements(obj,cursor):
    if obj.req != None:
        query = "INSERT INTO requirements (object_id, type, value) VALUES "
        for rq in obj.req:
            if " " in rq:
                typ, val = rq.split(" ")
            else:
                typ = rq
                val = 0
            query += f'({obj.id}, "{typ}", {val}),'
        query = query[:-1]+";" # required to do magic for later
        cursor.execute(query)
        # print(query)
    
    return obj


def create_obj(obj, cursor): #item: Item
    query = "INSERT INTO objects (name, effect) VALUES (%s, %s);"
    cursor.execute(query, (obj.name, obj.effect))
    obj.id = cursor.lastrowid # needed in order to have an id for the next step
    add_requirements(obj,cursor)
    return obj


# Route to create an item
# @app.post("/items/", response_model=Item)
def create_item(obj: Item, cursor): #item: Item
    create_obj(obj,cursor)
    if obj.tags != None:
        query = "INSERT INTO items (id, cost, craft) VALUES (%s,%s,%s); INSERT INTO item_tags (item_id, name, value) VALUES "
        for tag in obj.tags:
            if " " in tag:
                typ, val = tag.split(" ")
            else:
                typ = tag
                val = 0
            query += f'({obj.id}, "{typ}", {val}),'
        query = query[:-1]+";" # required to do magic for later
        cursor.execute(query, (obj.id, obj.cost, obj.craft))
        # print(query)
    return obj

def create_trait(obj: Trait, cursor): #item: Item
    create_obj(obj,cursor)
    query = "INSERT INTO traits (id, dice, is_passive) VALUES (%s,%s,%s)"
    cursor.execute(query, (obj.id, obj.dice, obj.is_passive))
    return obj



def add_spell_tags(obj: Spell, cursor): #item: Item
    if obj.tags != None:
        query = "INSERT INTO spell_tags (spell_id, name) VALUES "
        for tag in obj.tags:
            query += f'({obj.id}, "{tag}"),'
        query = query[:-1]+";" # required to do magic for later
        cursor.execute(query)
        # print(query)
    return obj


def create_spell(obj, cursor): #item: Item
    query = "INSERT INTO spells (name, effect, dice, level) VALUES (%s, %s, %s, %s);"
    cursor.execute(query, (obj.name, obj.effect, obj.dice, obj.level))
    obj.id = cursor.lastrowid # needed in order to have an id for the next step
    add_spell_tags(obj,cursor)
    return obj





# Route to read an item
# @app.get("/items/{item_id}", response_model=Item)
def read_object(object_id):
    cursor = conn.cursor()
    try:
        err = "ID"
        query = f"SELECT id, name, effect FROM objects WHERE id={int(object_id)}"
    except:
        err = "NAME"
        query = f'SELECT id, name, effect FROM objects WHERE name="{object_id}"'

    cursor.execute(query)
    item = cursor.fetchone()

    query = f"SELECT type, value FROM requirements WHERE object_id={item[0]}"
    cursor.execute(query)
    req = cleanup_tags(cursor.fetchall())

    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "effect": item[2],"req":req}


def cleanup_tags(tags):
    t = []
    for tag in tags:
        if len(tag) == 2:
            t.append(f"{tag[0]} {tag[1]}")
        else:
            t.append(str(tag[0]))
    return t

def read_spell(spell_quiry):
    cursor = conn.cursor()
    try:
        err = "ID"
        query = f"SELECT id, name, effect, dice, level FROM spells WHERE id={int(spell_quiry)}"
    except:
        err = "NAME"
        query = f'SELECT id, name, effect, dice, level FROM spells WHERE name="{spell_quiry}"'
    
    cursor.execute(query)
    item = cursor.fetchone()
    
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item not found with {err} lookup")
    
    query = f"SELECT name FROM spell_tags WHERE spell_id={item[0]}"
    cursor.execute(query)
    tags = cleanup_tags(cursor.fetchall())
    cursor.close()
    return {"id": item[0], "name": item[1], "effect": item[2], "dice": item[3], "level": item[4], "tags":tags}



obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])
obj = Trait("Fishman","you become manfish", ["body 1","mind 1"],0)
obj = Spell("poprocks","Boom Bam Bop", 2, 0,["ranged","attack"])
# create(obj)

# print(create_object(obj).id)

print(read_object("Fishman"))

print(read_spell(4))

# cursor = conn.cursor()
# query = "SELECT * FROM objects"
# cursor.execute(query)
# item = cursor.fetchall() # get all
# cursor.close()
# print(item)