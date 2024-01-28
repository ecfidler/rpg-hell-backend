import MySQLdb
from models import Object, Item, Trait, Spell, DBUser, Creature

from data_con_modules.data_core import conn
from data_con_modules.data_con_create import create_obj, create_item, create_spell, create_trait, create_creature

from data_con_modules.data_core import get_db_config

#######################################################################
########################## Creation Commands ##########################
#######################################################################


def create(obj, _id: int = None):
    conn = MySQLdb.connect(**get_db_config())
    # cursor = conn.cursor()
    print("Start Creation")

    try:
        clss = obj.__class__

        if clss == Object:
            print("Creating Obj")
            obj = create_obj(obj, conn, _id)
        # match (switch) cases dont work for objects aparently
        elif clss == Item:
            print("Creating Item")
            obj = create_item(obj, conn, _id)
        elif clss == Trait:
            print("Creating Trait")
            obj = create_trait(obj, conn, _id)
        elif clss == Spell:
            print("Creating Spell")
            obj = create_spell(obj, conn, _id)
        elif clss == Creature:
            print("Creating Creature")
            obj = create_creature(obj, conn, _id)
        else:
            raise TypeError("it broke, no give item")
        
        if obj == -1:
            raise Exception(f"Error occured in {clss}")

        # cursor.close()
        conn.commit()
        conn.close()
        print("Creation Successful")
        return obj.id

    except:
        # print(f"Error occured in {clss}")
        # cursor.close()
        conn.rollback()
        conn.close()
        return -1


def create_user(obj: DBUser, _id: int = None):
    query = f'INSERT INTO users (discord_id,`name`,email) VALUES ("{obj.discord_id}","{obj.username}","{obj.email}");'
    if _id:
        query = f'INSERT INTO users (id,discord_id,`name`,email) VALUES ({_id},"{obj.discord_id}","{obj.username}","{obj.email}");'

    cursor = conn.cursor()

    try:
        cursor.execute(query)
        # needed in order to have an id for the next step
        obj.id = cursor.lastrowid
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
        print(query)
        raise Exception("Creation user Broke")
    return obj
