from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:hoya@test-ghtwr.mongodb.net/test?retryWrites=true&w=majority")

print(client.test)

db = client["test_database"]
collection = db["test_collection"]

test_dict = {"name": "Alex"}

x = collection.insert_one(test_dict)
