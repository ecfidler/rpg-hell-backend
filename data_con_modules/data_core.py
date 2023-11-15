from settings import get_settings


settings = get_settings()

db_config = {"host": settings.database_host, "user": settings.database_user,
             "passwd": settings.database_password, "db": settings.database_name}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)


def send_query_return_all(query):
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        lst = cursor.fetchall() # gives a list of all info
        cursor.close()
        conn.commit()
        return lst
    except:
        cursor.close()
        conn.rollback()
        print(query)
        Exception("Creation user Broke")
    

def send_query_return_obj(query,obj):
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)
        obj.id = cursor.lastrowid  # needed in order to have an id for the next step
        cursor.close()
        conn.commit()
        return obj
    except:
        cursor.close()
        conn.rollback()
        print(query)
        Exception("Creation user Broke")