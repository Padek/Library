from fastapi import HTTPException
from pymongo import ReturnDocument

# Local imports
from library.config import books_collection, id_tracker_collection
from .models import Book, BookCreate, BookUpdate

def get_next_id():
    return id_tracker_collection.find_one_and_update(
        {"_id": "book_id"},
        {"$inc": {"next_id": 1}},
        return_document=ReturnDocument.AFTER
    )["next_id"]

def create_book_in_db(book: BookCreate):
    book_id = get_next_id()
    book_data = book.dict()
    book_data["id"] = book_id
    result = books_collection.insert_one(book_data)
    if result.inserted_id:
        return book_data
    raise HTTPException(status_code=500, detail="Book creation failed")

def get_all_books_from_db():
    books = list(books_collection.find())
    return books

def get_book_from_db(book_id: int):
    book = books_collection.find_one({"id": book_id})
    if book:
        return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")

def update_book_in_db(book_id: int, book: BookUpdate):
    result = books_collection.update_one({"id": book_id}, {"$set": book.dict()})
    if result.modified_count == 1:
        return get_book_from_db(book_id)
    raise HTTPException(status_code=404, detail="Book not found")

def delete_book_from_db(book_id: int):
    result = books_collection.delete_one({"id": book_id})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")