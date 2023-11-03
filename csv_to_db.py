from translator import *
import csv

def spliter(data):
    lst = str(data).lower().split(", ")
    return(lst)


def clean_csv(csv_path):
    with open(csv_path,'r') as f:
        clean = ''.join([i if ord(i) < 128 else ' ' for i in f.read()])

    with open(csv_path.replace(".csv","_clean.csv"),'w') as f:
        f.write(clean)

def get_dice(data):
    data = data.replace("Attack","##").replace("Contest","##").replace("11","##").replace("+","")
    
    dice = data.count("#")
    if "P" in data:
        return(dice*-1)
    return(dice)

def get_cost(data):
    d = data.split(", ")
    lvl = int(d[1].replace("St ",""))
    return get_dice(d[0]),lvl



def create_from_csv(csv_path):
    with open(csv_path, newline='') as f:
        reader = list(csv.reader(f))
        

        typ = 0 # defaults to spells
        if 'Dice Cost' in reader[0]: # check for trait
            typ = 1 
        elif "Defence" in reader[0]: # check for armor
            typ = 2
        elif "Fists" in reader[1]: # check for weapons
            typ = 3
        elif "Craft" in reader[0]: # check for items
            typ = 4


        for row in list(reader)[1:]: # skip the header
            obj = None
            
            if typ == 0:
                # Name,Cost,Effect,Tags
                print(f"Making Spell {row[0]}")
                dice, level = get_cost(row[1])
                tags = spliter(row[3])
                obj = Spell(row[0],row[2],dice,level,tags)
            elif typ == 1:
                # Name,Requirements,Dice Cost,Effect
                print(f"Making Trait {row[0]}")
                req = spliter(row[1])
                dice = get_dice(row[2])
                is_p = False
                if dice < 0:
                    dice = dice*-1
                    is_p = True
                obj = Trait(row[0],row[3],req,dice,is_p)
            elif typ == 2:
                # Name,Requirement,Effect,Defence,Traits
                print(f"Making Armor {row[0]}")
                req = spliter(row[1])
                tags = spliter(row[4])
                obj = Item(row[0],"",0,0,tags,req)
            elif typ == 3:
                # Name,Requirement,Tags,Effect
                print(f"Making Weapon {row[0]}")
                req = spliter(row[1])
                tags = spliter(row[2])
                obj = Item(row[0],row[3],0,0,tags,req)
            else:
                # Name,Tags,Effect,Cost,Crafting
                print(f"Making Item {row[0]}")
                tags = spliter(row[1])
                obj = Item(row[0],row[2],0,0,tags)
            
            # print(obj.return_data())
            
            create(obj)
            # print(f"Successfuly made {row[0]}")
        


if __name__ == "__main__":
    pass
    # create_from_csv('Rpg-Hell-db/Armor_all.csv')
    # create_from_csv("Rpg-Hell-db/Weapons_all.csv")

    # create_from_csv("Rpg-Hell-db/Traits_all.csv")
    

    # MAGIC ERROR
    # clean_csv("Rpg-Hell-db/Items_all.csv")
    # create_from_csv("Rpg-Hell-db/Items_all.csv")
    create_from_csv("Rpg-Hell-db/Spells_all.csv")