import os

import pymongo
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
FERNET_KEY = os.getenv("FERNET_KEY")
cluster = pymongo.MongoClient(f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_CONNECTION_STRING}/?retryWrites=true&w=majority")
database = cluster["valorant_logins"]


def add_user(username, password, region):
    if not check_user_existence(username, region):
        collection = database[region]
        password = encrypt_password(password)
        user = {
            "username": username,
            "password": password
        }
        collection.insert_one(user)
        return True
    return False


def encrypt_password(password):
    password = Fernet(FERNET_KEY).encrypt(password.encode("utf-8"))
    return password


def update_password(username, password, region):
    if check_user_existence(username, region):
        password = encrypt_password(password)
        collection = database[region]
        collection.update_one(
            {"username": username},
            {"$set": {"password": password}})
        return True
    return False


def check_user_existence(username, region):
    return bool(get_user(username, region))


def get_user(username, region):
    collection = database[region]
    user = collection.find_one({"username": username})
    if user is None:
        return False
    user["password"] = (Fernet(FERNET_KEY).decrypt(user["password"])).decode("utf-8")
    return user


def delete_user(username, region):
    collection = database[region]
    collection.delete_one({"username": username})
    return True
