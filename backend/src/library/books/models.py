from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: str

class BookRead(BookBase):
    image_path: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class Book(BookRead):
    id: int
