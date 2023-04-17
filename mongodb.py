import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://jackwrion12345:trongtin2002@jwrcluster.ucweufu.mongodb.net/test")
mydb = myclient["DoAnDaNganhDB"]
MemberColl = mydb["Member"]


def getInfo(ID):
    ID = str(ID)

    if MemberColl.count_documents({'ID': ID}) == 0:
        return
    else:
        mydoc = MemberColl.find({'ID': ID})
        return mydoc.next()

def addMember(image_input, name_input, ID_input):
    MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 0, 'date':  datetime.now() }  )
    return image_input
