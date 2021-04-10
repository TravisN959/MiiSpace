import pymongo
from pymongo import MongoClient


client = pymongo.MongoClient("mongodb+srv://DryadFam:Dryad@cluster0.laurd.mongodb.net/MiiSpace?retryWrites=true&w=majority")
database=client.MiiSpace
collection = database.AccountInfo



#username = String, password = String, bgImage = list(String), 
#pictures = list(tuple(String, tuple(x,y))), sticky_notes = list(tuple(String, tuple(x,y)))

#remember to make default values in signup function
def setupAccount(username, password, phone, name, bgImage=[], pictures=[], sticky_notes=[]):
    acct = {
        "username" : username,
        "password" : password,
        "bgImage" : bgImage,
        "pictures" : pictures,
        "sticky_notes" : sticky_notes,
        "phone" : phone,
        "name" : name,
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


def setUsername(oldUser, newUser):
    collection.update_one({"username": oldUser}, {"$set":{"username": newUser}})
    
def addImage(name,new_image):
    images=(collection.find_one({"username": name})['pictures'])
    images.append(new_image.filename)
    collection.update_one({ "username": name },{"$set": { "pictures": images }})

def resetImage(name):
    pics = []
    collection.update_one({ "username": name },{"$set": { "pictures": pics }})

def setPassword(username, password):
    collection.update_one({"username": username}, {"$set":{"password": password}})

def setName(username, name):
    collection.update_one({"username": username}, {"$set":{"name": name}})

def setPhone(username, phone):
    collection.update_one({"username": username}, {"$set":{"phone": phone}})
    
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






