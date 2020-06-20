from sanic import Sanic, response
from pymongo import MongoClient


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
            if ("username" in body) and ("password" in body):
                username = body.get("username")
                password = body.get("password")
                the_user_we_found = users.find_one({"username": username, "password": password})
                if action == "signup":
                    if the_user_we_found == None:
                        new_user = {
                            "username": username,
                            "password": password,
                        }
                        users.insert_one(new_user)
                        result["status"] = "ok: account has been created"
                    else:
                        result["status"] = "wrong: account has already been created"
                elif action == "login":
                    if the_user_we_found == None:
                        result["status"] = "wrong: no account or wrong password"
                    else:
                        result["status"] = "ok: logged in"
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
