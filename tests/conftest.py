import pytest
import sys, os
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app
from model import Base
from dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# client = TestClient(app)

# @pytest.fixture
# def test_client():
    
#     app.dependency_overrides[get_db] = lambda : "fake session"
#     with client:
#         yield client

#     app.dependency_overrides.clear()

# Database_test = "postgresql://postgres:password@localhost:5432/tests"
Database_test = "sqlite:///./test.db"

eng = create_engine(Database_test)

Session_test = sessionmaker(bind = eng, autoflush= False, autocommit = False)

# Base.metadata.create_all(bind = eng)

@pytest.fixture
def test_client():
    Base.metadata.drop_all(bind = eng)
    Base.metadata.create_all(bind = eng)

    def override_getdb():
        db = Session_test()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_getdb

    with TestClient(app) as c:
        yield c