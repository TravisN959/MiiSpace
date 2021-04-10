import pymongo
from pymongo import MongoClient


client = pymongo.MongoClient("mongodb+srv://DryadFam:Dryad@cluster0.laurd.mongodb.net/MiiSpace?retryWrites=true&w=majority")
database=client.MiiSpace
collection = database.AccountInfo



#username = String, password = String, bgImage = list(String), 
#pictures = list(tuple(String, tuple(x,y))), sticky_notes = list(tuple(String, tuple(x,y)))

#remember to make default values in signup function
def setupAccount(username, password, bgImage=[], pictures=[], sticky_notes=[]):
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

def addNote(name,new_text):
    notes=(collection.find_one({"username": name})['sticky_notes'])
    notes.append(new_text)
    collection.update_one({ "username": name },{"$set": { "sticky_notes": notes }})

def resetNote(name):
    notes=[]
    collection.update_one({ "username": name },{"$set": { "sticky_notes": notes }})



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






