from fastapi import APIRouter, Depends
from typing import List

# Local imports
from .services import (
    create_book_in_db,
    get_all_books_from_db,
    get_book_from_db,
    update_book_in_db,
    delete_book_from_db
)
from .models import Book, BookCreate, BookUpdate
from library.users.services import get_current_user

books = APIRouter()

@books.post("", response_model=Book, dependencies=[Depends(get_current_user)])
def create_book(book: BookCreate):
    return create_book_in_db(book)

@books.get("", response_model=List[Book])
def get_all_books():
    return get_all_books_from_db()

@books.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    return get_book_from_db(book_id)

@books.put("/{book_id}", response_model=Book, dependencies=[Depends(get_current_user)])
def update_book(book_id: int, book: BookUpdate):
    return update_book_in_db(book_id=book_id, book=book)

@books.delete("/{book_id}", dependencies=[Depends(get_current_user)])
def delete_book(book_id: int):
    return delete_book_from_db(book_id)