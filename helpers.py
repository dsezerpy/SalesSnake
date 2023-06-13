from pymongo import MongoClient
from passlib.context import CryptContext
from flask.app import HTTPException
from datetime import timedelta, datetime
import jwt
import os

database = MongoClient(os.getenv("SS_MONGODB_CONNSTR"))[os.getenv("SS_MONGODB_DATABASE")]
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Item:
    def __init__(self, category, name, unit, stock_amount, avg_value, nameid):
        self.category = category
        self.unit = unit
        self.stock_amount = stock_amount
        self.avg_value = f'{avg_value:.2f}'
        self.name = name
        self.total_value = f'{round(self.stock_amount * avg_value, 2):.2f}'
        self.nameid = nameid


def authenticate_user(email: str, password: str):
    user = database["users"].find_one({"email": email})
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return
    except:
        return
    user = database["users"].find_one({"email": email})
    if user is None:
        return
    return user


def register(user):
    if database["users"].find_one({"email": user["mail"]}):
        return 0
    database["users"].insert_one({
        "email": user["mail"],
        "password": get_password_hash(user["password"])
    })
    print("succ")
    return 1


def process_stocks(user):
    items = []
    total_price = 0
    for stock in database["stocks"].find({"user": user["_id"]}):
        total_price += stock["stock_size"] * stock["average_price"]
        items.append(
            Item(
                stock["category"], stock["displayname"], stock["unit"],
                stock["stock_size"], stock["average_price"], stock["nameid"]
            )
        )
    cats = [item['name'] for item in database["categories"].find({"user": user["_id"]})]
    total_price = f"{total_price:.2f}"
    units = database["units"].find_one({})["units"]
    today = f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}"
    return {"stocks": items, "cats": cats, "total_price": total_price,
            "currency": user['currency'], "units": units, "today": today}


def calc_weighted_avg(existing, new):
    existing["average_price"] = round(
        ((existing["average_price"] * existing["stock_size"]) + (int(new["avg_value"]) * int(new["stock"]))) / (
                existing["stock_size"] + int(new["stock"])), 2)
    existing["stock_size"] += int(new["stock"])
    return existing
