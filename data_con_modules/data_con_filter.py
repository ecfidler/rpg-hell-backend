
def cleanup_filter(items):
    ids = []
    for item in items:
        ids.append(item[0])
    return ids


def get_filter_query(loc: str, reqs: list[str]=[],tags: list[str]=[]):
    places = {"objects": "objects",
              "traits": "objects",
              "items": "objects",
              "spells": "spells"}
    place_tags = {"items": ["item_tags","item_id"], "spells": ["spell_tags","spell_id"]}

    query = f"SELECT DISTINCT id FROM {places[loc]} WHERE id IN ("
    # query = ""
    if len(reqs) == 1:
        name, val = reqs[0].split(" ")
        # SELECT DISTINCT id, name FROM objects WHERE id IN 
        # (SELECT object_id FROM requirements WHERE `type` IN ("body")
        # AND id IN 
        # (SELECT object_id FROM requirements GROUP BY object_id HAVING COUNT(*) = 1)
        # )
        query += f'''
                    (SELECT object_id FROM requirements WHERE `type` IN ("{name}") AND `value` IN ({val})
                    AND object_id IN (SELECT object_id FROM requirements GROUP BY object_id HAVING COUNT(*) = 1))
                '''
        
    elif len(reqs): # check for items in req
        query += "(SELECT object_id FROM requirements WHERE "
        first = True
        for req in reqs:
            name, val = req.split(" ")

            if not first:
                query += "AND "
            else:
                first = False

            query += f'object_id IN (SELECT object_id FROM requirements WHERE `type` IN ("{name}") AND `value` IN ({val})) '
        
        query = query[:-1]+") " # lop off extra space and add end
    
    if len(tags): # check for items in req
        if len(reqs): # this does not work... sql bullll
            query += "AND "

        query += f"(SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE "
        first = True
        for tag in tags:
            if not first:
                query += "AND "
            else:
                first = False

            try:
                name, val = tag.split(" ")
                query += f'{place_tags[loc][1]} IN (SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE `name` IN ("{name}") AND `value` IN ({val})) '
        
            except: # for spells
                query += f'{place_tags[loc][1]} IN (SELECT {place_tags[loc][1]} FROM {place_tags[loc][0]} WHERE `name` IN ("{tag}")) '
            
        query = query[:-1]+") " # lop off extra space and add end

    query = query[:-1]+")"
    
    return query