from user_management import app
import json
from logzero import logger
import hashlib
import random
import pprint
import gridfs


# clean database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.my_app
users = db.users
conversations = db.conversations
file_system = gridfs.GridFS(db)

#_id = "5e84d5d7cc38325cd8b5523b"
#v = file_system.exists(_id)
# print(_id)
# print(v)
# for f in file_system.find({}):
#    print(f._id)
#    print(type(f))
# exit()

username = "test"
password = "test"

salt = username[(len(username)//2):]
sha256_password = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()

temp_token = ""
name_list = []


def test_user_register():
    for name in ["hi", "leeo", "go", "you"]:
        username = name
        password = "test"
        salt = username[(len(username)//2):]
        sha256_password = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()

        body = {
            "username": username,
            "sha256_password": sha256_password,
        }
        data = {
            "action": "signup",
            "body": body,
        }
        request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

        logger.debug(type(response.json))
        logger.debug(response.json)
        assert "ok" in response.json.get("status"), f"response.json['status']"


def test_user_sign_up():
    body = {
        "username": username,
        "sha256_password": sha256_password,
    }
    data = {
        "action": "signup",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"


def test_user_log_in():
    global temp_token
    body = {
        "username": username,
        "sha256_password": sha256_password,
    }
    data = {
        "action": "login",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"
    temp_token = response.json.get("result").get("temp_token")
    logger.debug(temp_token)
    assert temp_token and len(temp_token) == 64, "no temp_token received"


def test_get_contact_list():
    global name_list
    data = {
        "username": username,
        "temp_token": temp_token,
    }
    request, response = app.test_client.post("/api/v1/contactlist", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"
    name_list = response.json.get("result").get("name_list")
    assert name_list != None
    logger.debug(name_list)


def test_send():
    from_ = username
    to_ = random.choice(name_list)
    text = f"Hello, {to_}"

    content = {
        "type": "text",
        "name": hashlib.sha256(text.encode("utf-8")).hexdigest()[:10],
        "file": text,
    }
    body = {
        # "from": from_,
        "to": to_,
        "content": content,
    }
    data = {
        "username": username,
        "temp_token": temp_token,
        "body": body,
    }

    request, response = app.test_client.post("/api/v1/send", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"


def get_file_by_id(data, _id):
    data['body'] = {
        "file_id": _id,
    }
    request, response = app.test_client.post("/api/v1/file", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"
    assert "result" in response.json
    return response.json.get("result")


def test_receive_one():
    target = random.choice(name_list)

    body = {
        "target": target,
    }
    data = {
        "username": username,
        "temp_token": temp_token,
        "body": body,
    }

    request, response = app.test_client.post("/api/v1/receive", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    #assert "ok" in response.json.get("status"), f"response.json['status']"
    if "ok" in response.json.get("status"):
        result = response.json.get("result")
        assert "history" in response.json.get("result")[0], response.json.get("result")
        assert "content" in response.json.get("result")[0].get("history")[0], response.json.get("result")
        content = response.json.get("result")[0].get("history")[0].get("content")
        assert "file_id" in content, response.json.get("result")
        get_file_by_id(data, content['file_id'])
    else:
        status = response.json.get("status")
        print(status)
        assert "no record" in status, status


def test_receive_all():
    target = ""

    body = {
        "target": target,
    }
    data = {
        "username": username,
        "temp_token": temp_token,
        "body": body,
    }

    request, response = app.test_client.post("/api/v1/receive", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    #assert "ok" in response.json.get("status"), f"response.json['status']"
    if "ok" in response.json.get("status"):
        result = response.json.get("result")
        pprint.pprint(result)
        assert "history" in response.json.get("result")[0], response.json.get("result")
    else:
        status = response.json.get("status")
        print(status)
        assert "no record" in status, status


def test_user_deletion():
    body = {
        "username": username,
        "sha256_password": sha256_password,
    }
    data = {
        "action": "delete",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"


def test_clean_up_the_mess():
    body = {
        "username": username,
        "sha256_password": sha256_password,
    }
    data = {
        "action": "delete",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    conversations.delete_many({})
    for f in file_system.find({}):
        print(f._id)
        file_system.delete(f._id)

    users.delete_many({})


if __name__ == "__main__":
    test_clean_up_the_mess()
    test_user_register()
    test_user_sign_up()
    test_user_log_in()
    for i in range(20):
        test_get_contact_list()
        test_send()
        test_receive_one()
        test_receive_all()
    test_clean_up_the_mess()
