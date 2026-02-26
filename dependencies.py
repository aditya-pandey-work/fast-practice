from db import SessionLocal
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from auth import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from model import User

s = HTTPBearer()

def get_db():
    database = SessionLocal()   
    try:
        yield database
    finally:
        database.close()

def get_curr_user(cred: HTTPAuthorizationCredentials = Depends(s), db: Session = Depends(get_db)):
    try:
        token = cred.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=400, detail="token is not valid")

    db_user = db.query(User).filter(User.id == user_id).first()

    # if not db_user:
    #     raise HTTPException(status_code=400, detail="user does not exists")
    
    return db_user  