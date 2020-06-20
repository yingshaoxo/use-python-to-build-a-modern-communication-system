from sanic import Sanic, response
from pymongo import MongoClient
import hashlib
import random
import string


client = MongoClient('mongodb://localhost:27017/')
db = client.my_app
users = db.users


app = Sanic(name="user_manager")


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
    app.run(host="0.0.0.0", port=8000, debug=True)
