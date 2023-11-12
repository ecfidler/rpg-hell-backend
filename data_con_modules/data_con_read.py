

def cleanup_tags(tags):
    t = []
    for tag in tags:
        if len(tag) == 2:
            t.append(f"{tag[0]} {tag[1]}")
        else:
            t.append(str(tag[0]))
    return t




def tag_type(tag):
    try:
        return (tag[1], tag[2])
    except:
        return (tag[1],)
    

def cleanup_bits_bobs(objects,tags,typ):
    tag_lst = {}
    t = []
    _id = tags[0][0]  # get the first id

    for tag in tags:
        if tag[0] != _id:
            tag_lst[_id] = t
            t = [tag_type(tag)]
            _id = tag[0]
        else:
            t.append(tag_type(tag))

    tag_lst[_id] = t
    
    for obj in objects:
        obj[typ] = []

        if obj["id"] in tag_lst:
            obj[typ] = cleanup_tags(tag_lst[obj["id"]])
    
    return objects


def cleanup_search(items, types = "types"):
    data, ids = [], []
    for item in items:

        info = {"id": item[0], "name": item[1], "effect": item[2],
                "dice": item[3], "is_passive": item[4]}
        if types == "items":
            info = {"id": item[0], "name": item[1],
                "effect": item[2], "cost": item[3], "craft": item[4]}
        elif types == "spells":
            info = {"id": item[0], "name": item[1],
                "effect": item[2], "dice": item[3], "level": item[4]} 

        data.append(info)
        ids.append(item[0])
    return data, ids

