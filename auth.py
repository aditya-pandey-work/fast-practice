from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "thiskeyisprivatepleasedontreadit"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE = 30

con = CryptContext(schemes=['bcrypt'])


def hashing_password(password: str):
    return con.hash(password)

def verify_password(password:str, hashed_pass: str):
    return con.verify(password, hashed_pass)

def create_access_token(data: dict):
    enco = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    enco.update({"exp": expire})
    return jwt.encode(enco, SECRET_KEY, algorithm=ALGORITHM)