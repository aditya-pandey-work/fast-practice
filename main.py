from fastapi import FastAPI, Depends, HTTPException
import json
from schema import Register
from sqlalchemy.orm import Session
from db import SessionLocal, my_engine
from dependencies import get_db
from model import User, Base
from auth import hashing_password, verify_password, create_access_token
import journal

app = FastAPI()

if __name__ == "__main__":
    Base.metadata.create_all(bind = my_engine)
app.include_router(journal.router, prefix="/api")

# def load_data(file):
#     return json.load(file)

# @app.get("/")
# def get_value():
#     with open("/home/lap-49/Documents/fast-practice/demo.json", "r") as f:
#         data = load_data(f)
    
#     return data["P01"]

@app.post("/register")
def register(user: Register, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="user already exists")
    
    db_user = User(
        username = user.username, 
        hash_password = hashing_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "registered"}

@app.post("/login")
def login_user(user: Register, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hash_password):
        raise HTTPException(status_code=400, detail="invalid details")
    
    token = create_access_token({"sub": str(db_user.id)})
    return {"access token": token , "token_type": "bearer"}

@app.get("/helo")
def hello():
    return {"message": "hello how are you!"}