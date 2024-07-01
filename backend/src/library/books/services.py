from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId

#Local imports
from library.config import books_collection
from .models import Book


async def create_book_in_db(book: Book):
    result = await books_collection.insert_one(book.model_dump())
    if result.inserted_id:
        return book
    raise HTTPException(status_code=500, detail="Book creation failed")


async def get_all_books_from_db():
    books = await books_collection.find().to_list(1000)
    return books


async def get_book_from_db(book_id: str):
    try:
        book = await books_collection.find_one({"_id": ObjectId(book_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if book:
        return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")


async def update_book_in_db(book_id: str, book: Book):
    try:
        result = await books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": book.dict()})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if result.modified_count == 1:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


async def delete_book_from_db(book_id: str):
    try:
        result = await books_collection.delete_one({"_id": ObjectId(book_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid book ID format")
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")