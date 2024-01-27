from data_con_modules.data_core import do_query


def delete_core(id: int, loc: str, conn):
    id_types = {"spells": "id",
                "spell_tags": "spell_id",
                "traits": "id",
                "objects": "id",
                "item_tags": "item_id",
                "items": "id",
                "requirements": "object_id",
                "users": "id",
                "creatures": "id",
                "creature_types": "creature_id"}

    query = f"DELETE FROM {loc} WHERE {id_types[loc]}={id}"
    # print(query)
    qItem = do_query(query,conn)
    if qItem == -1: # check error
        return -1
    return 1

