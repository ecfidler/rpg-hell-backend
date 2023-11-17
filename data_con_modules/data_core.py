
import MySQLdb
from settings import get_settings


settings = get_settings()

db_config = {"host": settings.database_host, "user": settings.database_user,
             "passwd": settings.database_password, "db": settings.database_name}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)

#######################################################################
############################## Mysc Tools #############################
#######################################################################


def spliter(data):
    lst = str(data).lower().split(", ")
    return (lst)


def do_query(query):
    cursor = conn.cursor()

    cursor.execute(query)
    item = cursor.fetchall()

    cursor.close()
    return item
