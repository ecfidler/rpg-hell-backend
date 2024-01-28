
import MySQLdb
import logging
from settings import get_settings


def get_db_config():
    settings = get_settings()

    db_config = {"host": settings.database_host, "user": settings.database_user,
                "passwd": settings.database_password, "db": settings.database_name}

    return db_config


# Create a connection to the database
conn = MySQLdb.connect(**get_db_config())

logging.basicConfig(filename='./logs/query.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#######################################################################
############################## Mysc Tools #############################
#######################################################################


def spliter(data):
    lst = str(data).lower().split(", ")
    return (lst)


def do_query(query, conn):
    logging.info('Starting new Query')
    logging.debug(query)
    # print(query)

    # conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        item = cursor.fetchall()

        # conn.commit()
        cursor.close()
        # conn.close()
    except Exception as e:
        logging.error("Error occured, Rolling back.")
        logging.error(e)

        # conn.rollback()
        cursor.close()
        # conn.close()
        return -1
    
    logging.info('Success Query')

    return item



def do_query_one(query,conn):
    logging.info('Starting new Query')
    logging.debug(query)

    # conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        item = cursor.fetchone()

        # conn.commit()
        cursor.close()
        # conn.close()
    except Exception as e:
        logging.error("Error occured, Rolling back.")
        logging.error(e)

        # conn.rollback()
        cursor.close()
        # conn.close()
        return -1
    
    logging.info('Success Query')

    return item


def do_query_lastID(query, conn):
    logging.info('Starting new Query')
    logging.debug(query)

    # conn = MySQLdb.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        item = cursor.lastrowid

        # conn.commit()
        cursor.close()
        # conn.close()
    except Exception as e:
        logging.error("Error occured, Rolling back.")
        logging.error(e)

        # conn.rollback()
        cursor.close()
        # conn.close()
        return -1
    
    logging.info('Success Query')

    return item
