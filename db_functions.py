import pymongo, uuid, hashlib
from pymongo import MongoClient
from datetime import datetime
import os
cluster = MongoClient(os.environ['MONGO_CLIENT'])
db = cluster["ARSNews"]
user_info = db["user-info"]
posts = db["posts"]
events = db["events"]
images = db["images"]
sha256_hash = hashlib.sha256()

class userFunctions():
    def __init__(self):
        pass
    def calc_sha(self, input_string):
        hashString = hashlib.sha256(input_string.encode()).hexdigest()
        return str(hashString)

    def checkID(self, typeID, value):
        if user_info.find_one({typeID: value}):
            return True
        else:
            return False

    def listUser(self):
        users = []
        for i in user_info.find({}):
            users.append(i)
        return users

    def deleteUser(self, id):
        user_info.delete_one({"_id": id})

    def addUser(self, username, password):
        specialID = str(uuid.uuid4())
        sessionID = str(uuid.uuid4())
        while self.checkID("_id", specialID) == False and self.checkID("sessionID",self.calc_sha(sessionID)) == True:
            specialID = str(uuid.uuid4())
            sessionID = str(uuid.uuid4())
        if self.checkID("username", username ) == False:
            post = {"_id": specialID, "username": username, "password": self.calc_sha(password), "sessionID": self.calc_sha(sessionID)}
            user_info.insert_one(post)

    def login(self, username, password):
        user = user_info.find_one({"username": username})
        if user:
            if user["password"] == self.calc_sha(password):
                sessionID = str(uuid.uuid4())
                while self.checkID("_id", sessionID) == True:
                    sessionID = str(uuid.uuid4())

                user_info.update_one({"username": username}, {"$set": {"sessionID":self.calc_sha(sessionID)}})
                return sessionID
            else:
                return False
        else:
            return False

    def logout(self, sessionID):
        sessionID = str(uuid.uuid4())
        while self.checkID("_id", sessionID) == True:
                sessionID = str(uuid.uuid4())
        user_info.update_one({"sessionID": sessionID}, {"$set": {"sessionID":self.calc_sha(sessionID)}})

    def checkSession(self, sessionID):
        return self.checkID('sessionID', self.calc_sha(sessionID))

class postFunctions():

    def __init__(self):
        pass

    def checkID(self, typeID, value):
        if posts.find_one({typeID: value}):
            return True
        else:
            return False

    def addPost(self, title, active, caption, image, content):
        specialID = str(uuid.uuid4())
        while self.checkID("_id", specialID) == True:
            specialID = str(uuid.uuid4())
        time = datetime.now()
        time.strftime("%d %B, %Y")
        post = {"_id": specialID, "date": time.strftime("%d %B, %Y"), "title": title, "active": active, "caption": caption, "image": image, "content": content}
        posts.insert_one(post)

    def delPost(self, id):
        posts.update_one({"_id" : id}, {"$set":{"active":False}})

    def updatePost(self, id, title, caption, image, content):
        posts.update_one({"_id" : id}, {"$set":{"title":title}})
        posts.update_one({"_id" : id}, {"$set":{"caption":caption}})
        posts.update_one({"_id" : id}, {"$set":{"image":image}})
        posts.update_one({"_id" : id}, {"$set":{"content":content}})

    def getPosts(self):
        all_posts = []
        for i in posts.find({'active' : True}):
            all_posts.append(i)
        all_posts.reverse()
        return all_posts

    def getPost(self, id):
        return posts.find_one({"_id": id})

    def getContent(self, id):
        post = posts.find_one({"_id": id})
        return post['content']


class eventFunctions():

    def __init__(self):
        pass

    def checkID(self, typeID, value):
        if events.find_one({typeID: value}):
            return True
        else:
            return False

    def addEvent(self, title, active, caption, image, date):
        specialID = str(uuid.uuid4())
        while self.checkID("_id", specialID) == True:
            specialID = str(uuid.uuid4())
        event = {"_id": specialID, "title": title, "active": active, "caption": caption, "image": image, "date": date}
        events.insert_one(event)

    def delEvent(self, id):
        events.update_one({"_id" : id}, {"$set":{"active":False}})

    def updateEvent(self, id, title, caption, image, date):
        events.update_one({"_id" : id}, {"$set":{"title":title}})
        events.update_one({"_id" : id}, {"$set":{"caption":caption}})
        events.update_one({"_id" : id}, {"$set":{"image":image}})
        events.update_one({"_id" : id}, {"$set":{"date":date}})

    def getEvents(self):
        all_events = []
        for i in events.find({'active' : True}):
            all_events.append(i)
        all_events.reverse()
        return all_events

    def getEvent(self, id):
        return events.find_one({"_id": id})

class imageFunctions():

    def __init__(self):
        pass

    def checkID(self, typeID, value):
        if images.find_one({typeID: value}):
            return True
        else:
            return False

    def upload(self, title, location):
        specialID = str(uuid.uuid4())
        while self.checkID("_id", specialID) == True:
            specialID = str(uuid.uuid4())
        image = {"_id": specialID, "title": title, "location": location}
        images.insert_one(image)
        return specialID

    def getImage(self, id):
        return images.find_one({"_id": id})["location"]

    def getImages(self):
        all_images = []
        for i in images.find():
            all_images.append(i)
        all_images.reverse()
        return all_images

    def deleteImage(self, id):
        images.delete_one({"_id": id})
