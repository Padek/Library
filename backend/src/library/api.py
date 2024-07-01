from fastapi import APIRouter
from library.books.views import books as books_router
from library.users.views import auth as auth_router

api = APIRouter()

api.include_router(books_router, tags=["books"], prefix="/books")
api.include_router(auth_router, tags=["auth"], prefix="/auth")