import pymongo
import mongoKEYS

#Gets database
client = pymongo.MongoClient(mongoKEYS.getKEY())
database = client["MiiSpace"]

#Our specific database for this file
collection = database["AccountInfo"]


#username = String, password = String, bgImage = list(String), 
#pictures = list(tuple(String, tuple(x,y))), sticky_notes = list(tuple(String, tuple(x,y)))

#remember to make default values in signup function
def setupAccount(username, password, bgImage, pictures, sticky_notes):
    acct = {
        "username" : username,
        "password" : password,
        "bgImage" : bgImage,
        "pictures" : pictures,
        "sticky_notes" : sticky_notes,
    }
    collection.insert_one(acct)

def getInfo(username):
    return collection.find_one({"username": username})

def getAccounts():
    return collection.find({})


def checkDuplicateUsername(username):
    query = {
        "username" : username
    }
    found = collection.count_documents(query, limit = 1)

    if found != 0:
        return True
    else:
        return False


def validateLogin(username, password):
    query = {
        "username": username,
        "password": password
    }
    found = collection.count_documents(query, limit = 1)
    if found != 0:
        return True
    else:
        return False





