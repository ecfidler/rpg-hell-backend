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

    def __init__(self, _name, _effect, _req = []):
        self.name = _name
        self.effect = _effect
        self.req = _req
        

class Trait(Object):
    dice: int
    is_passive: bool = False
    
    def __init__(self, _name, _effect, _req, _dice, _is_passive = False):
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
    
    def __init__(self, _name, _effect, _cost, _craft, _tags, _req=[]):
        self.name = _name
        self.effect = _effect
        self.cost = _cost
        self.craft = _craft
        self.tags = _tags

        self.req = _req
    



def create(obj):
    cursor = conn.cursor()
    try:
        clss = obj.__class__
        if clss == Object:
            create_obj(obj, cursor)
        elif clss == Item: # match (switch) cases dont exist in this vs of python. Very sad
            create_item(obj, cursor)

        # Not implemented yet
        # elif clss == Trait:
        #     create_trait(obj, cursor)
            
        cursor.close()
        conn.commit()
    except:
        print("Error occured")
        cursor.close()
        conn.rollback()


def create_obj(obj, cursor): #item: Item
    query = "INSERT INTO objects (name, effect) VALUES (%s, %s);"
    cursor.execute(query, (obj.name, obj.effect))
    obj.id = cursor.lastrowid # needed in order to have an id for the next step
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

# Route to read an item
# @app.get("/items/{item_id}", response_model=Item)
def read_object(item_id: int):
    cursor = conn.cursor()
    query = "SELECT id, name, effect FROM objects WHERE id=%s"
    cursor.execute(query, (item_id,))
    item = cursor.fetchone()
    cursor.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item[0], "name": item[1], "effect": item[2]}



obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])

create(obj)

# print(create_object(obj).id)

# print(read_object(obj.id))

cursor = conn.cursor()
query = "SELECT * FROM objects"
cursor.execute(query)
item = cursor.fetchall() # get all
cursor.close()
print(item)