from sanic import Sanic, response
from sanic_cors import CORS
from pymongo import MongoClient
import hashlib
import random
import string
from datetime import datetime
import json
from bson import json_util
import pprint


client = MongoClient('mongodb://localhost:27017/')
db = client.my_app
users = db.users
conversations = db.conversations


app = Sanic(name="user_manager")
CORS(app)


@app.route('/api/v1/usermanagement', methods=['POST'])
async def user_management(request):
    data = request.json
    result = {"status": "ok"}
    if data:
        action = data.get("action")
        body = data.get("body")
        if action and body:
            if ("username" in body) and ("sha256_password" in body):
                username = body.get("username")
                sha256_password = body.get("sha256_password")
                the_user_we_found = users.find_one({"username": username, "sha256_password": sha256_password})

                if action == "signup":
                    if the_user_we_found == None:
                        new_user = {
                            "username": username,
                            "sha256_password": sha256_password,
                        }
                        users.insert_one(new_user)
                        result["status"] = "ok: account has been created"
                    else:
                        result["status"] = "wrong: account has already been created"
                elif action == "login":
                    if the_user_we_found == None:
                        result["status"] = "wrong: no account or wrong password"
                    else:
                        random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                        random_string += username
                        temp_token = hashlib.sha256(random_string.encode("utf-8")).hexdigest()
                        users.find_one_and_update({"_id": the_user_we_found.get("_id")}, {"$set": {"temp_token": temp_token}})
                        result["status"] = "ok: logged in"
                        result["result"] = {"temp_token": temp_token}
                elif action == "delete":
                    if the_user_we_found == None:
                        result["status"] = "wrong: no account or wrong password"
                    else:
                        users.find_one_and_delete({"_id": the_user_we_found.get("_id")})
                        result["status"] = "ok: account has been deleted"
            else:
                result["status"] = "wrong: no username or password received"
        else:
            result["status"] = "wrong: no action or body received"
    else:
        result["status"] = "wrong: no json data received"
    return response.json(result)


@app.route('/api/v1/verify', methods=['POST'])
async def verify(request):
    data = request.json
    result = {"status": "wrong, you have to sign up or log in"}
    if data:
        username = data.get("username")
        temp_token = data.get("temp_token")
        if username and temp_token:
            the_user_we_found = users.find_one({"username": username, "temp_token": temp_token})
            if the_user_we_found != None:
                result["status"] = "ok"
    return response.json(result)


@app.route('/api/v1/contactlist', methods=['POST'])
async def get_contact_list(request):
    data = request.json
    result = {"status": "wrong"}
    if data:
        username = data.get("username")
        temp_token = data.get("temp_token")
        if username and temp_token:
            the_user_we_found = users.find_one({"username": username, "temp_token": temp_token})
            if the_user_we_found == None:
                result["status"] = "wrong: user doesn't exist"
            else:
                userlist = users.find({"_id": {"$nin": [the_user_we_found.get("_id")]}})
                #userlist = users.find({"username": {"$nin": [username]}})
                name_list = []
                for user in userlist:
                    name_list.append(user.get("username"))
                result["result"] = {"name_list": name_list}
                result["status"] = "ok"
    return response.json(result)


def update_an_conversation(from_, to_, text):
    date = datetime.datetime.utcnow()
    conversation_name = "_".join(list(sorted([from_, to_])))
    conversation = conversations.find_one({"conversation_name": conversation_name})
    if conversation == None:
        create_an_conversation(from_, to_, text, date)
    else:
        conversations.find_one_and_update({"_id": conversation.get("_id")}, {
            "$addToSet": {
                "history": {
                    "date": date,
                    "from": from_,
                    "to": to_,
                    "text": text,
                }
            }
        })


def create_an_conversation(from_, to_, text, date):
    conversation_name = "_".join(list(sorted([from_, to_])))
    conversation = {
        "conversation_name": conversation_name,
        "history": [
            {
                "date": date,
                "from": from_,
                "to": to_,
                "text": text,
            }
        ]
    }
    conversations.insert_one(conversation)


@app.route('/api/v1/send', methods=['POST'])
async def send(request):
    data = request.json
    result = {"status": "wrong"}
    if data:
        username = data.get("username")
        temp_token = data.get("temp_token")
        body = data.get("body")
        if username and temp_token and body:
            the_user_we_found = users.find_one({"username": username, "temp_token": temp_token})
            if the_user_we_found != None:
                from_ = username
                to = body.get("to")
                text = body.get("text")
                if to and text:
                    result["status"] = "ok"
                    update_an_conversation(from_, to, text)
                else:
                    result["status"] = "wrong: 'to' or 'text' not found at 'body'"
            else:
                result["status"] = "wrong: no such account or wrong temp_token"

    return response.json(result)


def get_conversation(username, target):
    data = None
    if target == "" or target:
        if target != "":
            conversation_name = "_".join(list(sorted([username, target])))
            conversation = conversations.find_one({"conversation_name": conversation_name})
            if conversation != None:
                data = [conversation]

        else:
            regex = "(" + username+"_.*)|(.*_"+username+")"
            many_conversations = conversations.find({"conversation_name": {"$regex": regex}})
            if many_conversations != None:
                result = []
                for conversation in many_conversations:
                    result.append(conversation)
                data = result
    return data


def my_json_dumps(data):
    # return json_util.dumps(data)
    return json.dumps(data, default=str)


@app.route('/api/v1/receive', methods=['POST'])
async def receive(request):
    data = request.json
    result = {"status": "wrong"}
    if data:
        username = data.get("username")
        temp_token = data.get("temp_token")
        body = data.get("body")
        if username and temp_token and body:
            the_user_we_found = users.find_one({"username": username, "temp_token": temp_token})
            if the_user_we_found != None:
                target = body.get("target")
                if target == "" or target:
                    got = get_conversation(username, target)
                    if got == None:
                        result["status"] = f"wrong: no record with {username}_{target}"
                    else:
                        result["status"] = "ok"
                        result["result"] = got
                else:
                    result["status"] = "wrong: 'target' not found at 'body'"
            else:
                result["status"] = "wrong: no such account or wrong temp_token"
    return response.json(result, dumps=my_json_dumps)


@app.route('/api/v1/communicate', methods=['POST'])
async def user_communicate(request):
    data = request.json
    result = {"status": "wrong"}
    if data:
        username = data.get("username")
        temp_token = data.get("temp_token")
        action = data.get("action")
        body = data.get("body")
        if username and temp_token and action and body:
            the_user_we_found = users.find_one({"username": username, "temp_token": temp_token})
            if action == "test":
                if the_user_we_found == None:
                    result["status"] = "wrong: no such account or wrong temp_token"
                else:
                    result["status"] = "ok"
                    result["result"] = {"msg": f"I got your msg: {str(body)}"}

    return response.json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
