target = body.get("target")
if target == "" or target:
	got = get_conversation(username, target)
	if got == None:
		result["status"] = f"wrong: no record with {username}_{target}"
	else:
		result["status"] = "ok"
		result["result"] = got