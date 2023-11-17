
import json
import MySQLdb
from fastapi import HTTPException, Query


from models import Object, Item, Trait, Spell

# from data_con_modules.data_con_create import create_obj, create_item, create_trait, create_spell
# from data_con_modules.data_con_update import update_item, update_spell, update_trait
# from data_con_modules.data_con_del import delete_core
# from data_con_modules.data_con_read import cleanup_search, cleanup_tags_req, read_one, read_list
# from data_con_modules.data_con_filter import cleanup_filter, get_filter_query

from settings import get_settings


settings = get_settings()

db_config = {"host": settings.database_host, "user": settings.database_user,
             "passwd": settings.database_password, "db": settings.database_name}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)





if __name__ == "__main__":
    pass
    # obj = Item('oh boy','its party time',6,1,['aaaa 20','ooo 1'])
    # obj = Trait("Fishman","you become manfish", ["body 1","mind 1"], 0)
    # obj = Spell("poprocks","Boom Bam Bop", 2, 0,["ranged","attack"])
    # create(obj)

    # print(create_object(obj).id)

    # print(read_object(1))

    # print(read_spell("poprocks"))
    # print(get_items())
    # print(get_traits())
    # print(get_spells([1]))

    # print(filter_base("spells",[],["touch"])) # Fails if given both at the same time but works seprately
    # print(filter_spells_by_tags(["touch","utility"]))
    # print(filter_traits_by_reqs(["soul 2","body 1"]))
    # print(filter_items_by_reqs(["body 2"]))
    # print(filter_items_by_tags(["tiny",'potion']))

    # ids = [477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629]

    # [{1,stuff},{3,stuff},{63,stuff}]
    # [[(1,name,val),(1,name,val)], [], [(63,name,val)],]

    # txt = ""
    # for a in ids:
    #     txt += f"({a}),"

    # print(txt)

    # print(read_spell(4))

    # cursor = conn.cursor()
    # query = "SELECT * FROM objects"
    # cursor.execute(query)
    # item = cursor.fetchall() # get all
    # cursor.close()
    # print(item)

    # print(delete_trait("Fishman"))
