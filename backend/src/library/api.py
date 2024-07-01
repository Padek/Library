from fastapi import APIRouter
from library.books.views import books as books_router

api = APIRouter()

api.include_router(books_router, tags=["books"], prefix="/books")