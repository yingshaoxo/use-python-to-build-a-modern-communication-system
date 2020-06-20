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