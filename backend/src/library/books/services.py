import os
from fastapi import HTTPException, UploadFile
from pymongo import ReturnDocument
import shutil

# Local imports
from library.config import books_collection, id_tracker_collection
from .models import Book, BookCreate, BookUpdate

def get_next_id():
    return id_tracker_collection.find_one_and_update(
        {"_id": "book_id"},
        {"$inc": {"next_id": 1}},
        return_document=ReturnDocument.AFTER
    )["next_id"]

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
IMAGE_DIR = "book_images"

# Ensure the image directory exists
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_book_in_db(book: BookCreate):
    book_id = get_next_id()
    book_data = book.model_dump()
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
    result = books_collection.update_one({"id": book_id}, {"$set": book.model_dump()})
    if result.modified_count == 1:
        return get_book_from_db(book_id)
    raise HTTPException(status_code=404, detail="Book not found")

def delete_book_from_db(book_id: int):
    result = books_collection.delete_one({"id": book_id})
    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

async def upload_book_image(book_id: int, file: UploadFile):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG and PNG files are allowed.")
    
    book = get_book_from_db(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    file_path = os.path.join(IMAGE_DIR, f"{book_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = books_collection.update_one({"id": book_id}, {"$set": {"image_path": file_path}})
    if result.modified_count != 1:
        raise HTTPException(status_code=500, detail="Failed to update book with image path.")
    
    return {"filename": file.filename}

async def get_book_image(book_id: int):
    book = get_book_from_db(book_id)
    if not book or not book.image_path:
        raise HTTPException(status_code=404, detail="Image not found for this book")
    
    return book.image_path