from pymongo import MongoClient
import datetime
import pprint

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
posts = db.posts
posts.delete_many({})

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}
post2 = {
    "author": "yingshaoxo",
    "text": "My first latex book!",
    "tags": ["mongodb", "python", "pymongo", "latex"],
    # "date": datetime.datetime.utcnow()
}

posts.insert_one(post)
posts.insert_one(post2)

post = posts.find_one({'author': 'Mike'})
print("Find one item from the database:")
pprint.pprint(post)
print('\n'*2)

posts.find_one_and_update({"_id": post.get("_id")}, {"$set": {"new_field": "888888888888888888888888888888888888888888888"}})

print("Find multiple items from the database:")
for post in posts.find():
    pprint.pprint(post)
    print()
print('\n'*2)

print(client.list_database_names())
