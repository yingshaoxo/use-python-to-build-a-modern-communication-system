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