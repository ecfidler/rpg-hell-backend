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

