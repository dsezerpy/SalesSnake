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
    total_value: int

    def __init__(self, category, name, unit, currency, stock_amount, avg_value):
        self.category = category
        self.unit = unit
        self.stock_amount = stock_amount
        self.avg_value = avg_value
        self.currency = currency
        self.name = name
        self.total_value = self.stock_amount * self.avg_value


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
