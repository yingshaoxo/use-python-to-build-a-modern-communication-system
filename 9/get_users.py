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