from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str

class JournalCreate(BaseModel):
    title: str
    content: str