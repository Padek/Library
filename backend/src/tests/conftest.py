import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from library.main import app
from library.config import books_collection, users_collection

@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function", autouse=True)
def clear_db():
    books_collection.delete_many({})
    users_collection.delete_many({})