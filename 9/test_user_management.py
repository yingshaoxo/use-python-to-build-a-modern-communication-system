from user_management import app
import json
from logzero import logger
import hashlib
import random
import pprint


# clean database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.my_app
users = db.users
# users.delete_many({})
conversations = db.conversations
# conversations.delete_many({})

#result = conversations.find({})
# for i in result:
#    print(type(i))
#    #print(dir(result))
# print(type(conversations.find_one({})))
# exit()

username = "test"
password = "test"

salt = username[(len(username)//2):]
sha256_password = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()

temp_token = ""
name_list = []


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


def test_user_communicate():
    body = {
        "msg": "hi"
    }
    data = {
        "username": username,
        "temp_token": temp_token,
        "action": "test",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/communicate", data=json.dumps(data))
    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"
    msg = response.json.get("result").get("msg")
    assert msg != None


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

    body = {
        "from": from_,
        "to": to_,
        "text": text,
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


if __name__ == "__main__":
    # test_user_sign_up()
    test_user_log_in()
    test_get_contact_list()
    # test_send()
    test_receive_one()
    test_receive_all()
    # test_user_deletion()
