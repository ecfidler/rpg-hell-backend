from data_connector import *
import csv


def clean_csv(csv_path):
    with open(csv_path, 'r') as f:
        clean = ''.join([i if ord(i) < 128 else ' ' for i in f.read()])

    with open(csv_path.replace(".csv", "_clean.csv"), 'w') as f:
        f.write(clean)


def get_dice(data):
    data = data.replace("Attack", "##").replace(
        "Contest", "##").replace("11", "##").replace("+", "")

    dice = data.count("#")
    if "P" in data:
        return (dice*-1)
    return (dice)


def get_cost(data):
    d = data.split(", ")
    lvl = int(d[1].replace("St ", ""))
    return get_dice(d[0]), lvl


def create_from_csv(csv_path):
    with open(csv_path, encoding="utf8", newline='') as f:
        reader = list(csv.reader(f))

        typ = 0  # defaults to spells
        if 'Dice Cost' in reader[0]:  # check for trait
            typ = 1
        elif "Defence" in reader[0]:  # check for armor
            typ = 2
        elif "Fists" in reader[1]:  # check for weapons
            typ = 3
        elif "Crafting" in reader[0]:  # check for items
            typ = 4

        for row in list(reader)[1:]:  # skip the header
            obj = None

            if typ == 0:
                # Name,Cost,Effect,Tags
                print(f"Making Spell {row[0]}")
                dice, level = get_cost(row[1])
                tags = spliter(row[3])
                obj = Spell(name=row[0], effect=row[2], dice=dice, level=level, tags=tags)
            elif typ == 1:
                # Name,Requirements,Dice Cost,Effect
                print(f"Making Trait {row[0]}")
                req = spliter(row[1])
                dice = get_dice(row[2])
                is_p = False
                if dice < 0:
                    dice = dice*-1
                    is_p = True
                obj = Trait(name=row[0], effect=row[3], req=req, dice=dice, is_passive=is_p)
            elif typ == 2:
                # Name,Requirement,Effect,Defence,Traits
                print(f"Making Armor {row[0]}")
                req = spliter(row[1])
                tags = spliter(row[4])
                obj = Item(name=row[0], effect="", cost=0, craft=0, tags=tags, req=req)
            elif typ == 3:
                # Name,Requirement,Tags,Effect
                print(f"Making Weapon {row[0]}")
                req = spliter(row[1])
                tags = spliter(row[2])
                obj = Item(name=row[0], effect=row[3], cost=0, craft=0, tags=tags, req=req)
            else:
                # Name,Tags,Effect,Cost,Crafting
                print(f"Making Item {row[0]}")
                tags = spliter(row[1])
                obj = Item(name=row[0], effect=row[2], cost=0, craft=0, tags=tags)

            # print(obj.return_data())

            create(obj)
            # print(f"Successfuly made {row[0]}")


if __name__ == "__main__":
    pass
    # create_from_csv('data/Armor_all1104.csv')
    # create_from_csv("data/Weapons_all1104.csv")

    # create_from_csv("data/Traits_all1105.csv")

    # MAGIC ERROR
    # clean_csv("data/Items_all.csv")
    create_from_csv("data/Items_all1105.csv")
    #create_from_csv("data/Spells_all1105.csv")
