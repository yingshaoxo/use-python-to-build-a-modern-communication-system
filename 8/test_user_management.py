from user_management import app
import json
from logzero import logger
import hashlib


# clean database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.my_app
users = db.users
users.delete_many({})


username = "yingshaoxo"
password = "hello"

salt = username[(len(username)//2):]
sha256_password = hashlib.sha256((password+salt).encode("utf-8")).hexdigest()

temp_token = ""


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
