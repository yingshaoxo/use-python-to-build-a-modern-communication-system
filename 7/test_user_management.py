from user_management import app
import json
from logzero import logger


def test_user_sign_up():
    username = "yingshaoxo"
    password = "hello"
    body = {
        "username": username,
        "password": password,
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
    username = "yingshaoxo"
    password = "hello"
    body = {
        "username": username,
        "password": password,
    }
    data = {
        "action": "login",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"


def test_user_deletion():
    username = "yingshaoxo"
    password = "hello"
    body = {
        "username": username,
        "password": password,
    }
    data = {
        "action": "delete",
        "body": body,
    }
    request, response = app.test_client.post("/api/v1/usermanagement", data=json.dumps(data))

    logger.debug(type(response.json))
    logger.debug(response.json)
    assert "ok" in response.json.get("status"), f"response.json['status']"
