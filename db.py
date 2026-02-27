from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os 

# load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL VALUE IS:", DATABASE_URL)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

my_engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind = my_engine, 
    autoflush= False, 
    autocommit = False
)