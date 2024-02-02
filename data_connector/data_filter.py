from data_con_modules.data_core import conn
from data_con_modules.data_con_filter import get_filter_query,cleanup_filter

from data_connector.data_read import get_traits_conn, get_items_conn, get_spells_conn, get_users


#######################################################################
########################### Filter Commands ###########################
#######################################################################


def filter_base(loc: str, reqs: list[str] = [], tags: list[str] = []):
    # SELECT DISTINCT id, name FROM objects WHERE id IN
    # (SELECT object_id FROM requirements WHERE
    # object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("Body") AND `value` IN (2))
    # AND object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("mind") AND `value` IN (1))
    # )

    cursor = conn.cursor()

    query = get_filter_query(loc, reqs, tags)

    print(query)
    cursor.execute(query)
    ids = cleanup_filter(cursor.fetchall())

    cursor.close()
    return ids


def filter_traits_by_reqs(reqs: list[str]):
    ids = filter_base("traits", reqs)
    if len(ids):
        data, ids = get_traits_conn(ids)
    else:
        return [], []

    return data, ids


def filter_items_by_reqs(reqs: list[str]):
    ids = filter_base("items", reqs)
    if len(ids):
        data, ids = get_items_conn(ids)
    else:
        return [], []

    return data, ids


def filter_items_by_tags(tags: list[str]):
    ids = filter_base("items", [], tags)
    if len(ids):
        data, ids = get_items_conn(ids)
    else:
        return [], []

    return data, ids


def filter_spells_by_tags(tags: list[str]):
    ids = filter_base("spells", [], tags)
    if len(ids):
        data, ids = get_spells_conn(ids)
    else:
        return [], []

    return data, ids
