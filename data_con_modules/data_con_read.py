

def cleanup_tags(tags):
    t = []
    for tag in tags:
        if len(tag) == 2:
            t.append(f"{tag[0]} {tag[1]}")
        else:
            t.append(str(tag[0]))
    return t


def cleanup_req_large(traits, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            t.append((tag[1], tag[2]))
        else:
            traits[loc]["req"] = cleanup_tags(t)
            loc += 1
            t = [(tag[1], tag[2])]
            _id = tag[0]

    traits[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return traits


def cleanup_item_req_large(items, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            t.append((tag[1], tag[2]))
        else:
            while items[loc]["id"] != _id:
                loc += 1
            items[loc]["req"] = cleanup_tags(t)
            loc += 1
            t = [(tag[1], tag[2])]
            _id = tag[0]

    while items[loc]["id"] != _id:
        loc += 1
    items[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return items


def cleanup_tags_large(items, tags):
    loc = 0  # so this is the item that tells what requirements go with what data
    _id = tags[0][0]  # get the first id
    t = []
    for tag in tags:
        if tag[0] == _id:
            try:
                t.append((tag[1], tag[2]))
            except:
                t.append((tag[1],))
        else:
            items[loc]["tags"] = cleanup_tags(t)
            loc += 1
            try:
                t = [(tag[1], tag[2])]
            except:
                t = [(tag[1],)]
            # t = [(tag[1], tag[2])]
            _id = tag[0]

    items[loc]["req"] = cleanup_tags(t)  # so we dont skip the last line

    return items


def cleanup_search_traits(items):
    data, ids = [], []
    for item in items:
        info = {"id": item[0], "name": item[1], "effect": item[2],
                "dice": item[3], "is_passive": item[4]}
        data.append(info)
        ids.append(item[0])
    return data, ids


def cleanup_search_items(items):
    data, ids = [], []
    for item in items:
        info = {"id": item[0], "name": item[1],
                "effect": item[2], "cost": item[3], "craft": item[4]}
        data.append(info)
        ids.append(item[0])
    return data, ids

