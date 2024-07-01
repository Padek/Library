from fastapi import FastAPI
from library.api import api


app = FastAPI(title="LibraryAPI")

app.include_router(api)
