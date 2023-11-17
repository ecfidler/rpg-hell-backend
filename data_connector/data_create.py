from models import Object, Item, Trait, Spell

from data_con_modules.data_core import conn
from data_con_modules.data_con_create import create_obj, create_item, create_spell, create_trait


#######################################################################
########################## Creation Commands ##########################
#######################################################################


def create(obj, _id: int = None):
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


def create_user(obj):
    cursor = conn.cursor()
    query = f"INSERT INTO users (discord_id,`name`) VALUES ({obj.id},{obj.name});"

    try:
        cursor.execute(query)
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        cursor.close()
        conn.commit()
    except:
        cursor.close()
        conn.rollback()
        print(query)
        raise Exception("Creation user Broke")
    return obj
