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
    MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 0, 'path' : image_input , 'type' : 'reg'  ,'date':  datetime.now() }  )
    return 0



def checkin(ID_input, name_input):
    doc = MemberColl.find( {'ID': ID_input } ).sort('_id',-1).limit(1)
    doc = doc.next()
    if doc['status'] == 0:
        MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 1, 'type' : 'in'  ,'date':  datetime.now() }  )
        return 0
    else:
        return 1


    

def checkout(ID_input, name_input):
    doc = MemberColl.find( {'ID': ID_input } ).sort('_id',-1).limit(1)
    doc = doc.next()
    if doc['status'] == 1:
        MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 0, 'type' : 'out'  ,'date':  datetime.now() }  )
        return 0
    else:
        return 1