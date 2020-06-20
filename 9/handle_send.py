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