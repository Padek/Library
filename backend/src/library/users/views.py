from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

# Local imports
from .models import Token
from .services import (
    register_user_on_db,
    log_in_user
)

auth = APIRouter()

@auth.post("/register")
async def register(username: str, password: str):
    return register_user_on_db(username=username, password=password)

@auth.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return log_in_user(form_data)
