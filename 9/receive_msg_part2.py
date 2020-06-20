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