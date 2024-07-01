from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from library.api import api
from library.logs import configure_logging

app = FastAPI(title="LibraryAPI")

app.include_router(api)

# Configure logs
configure_logging()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware to log requests and responses
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request details
        logging.info(f"Request: {request.method} {request.url}")

        try:
            response = await call_next(request)
            # Log response details
            logging.info(f"Response: {response.status_code} for {request.method} {request.url}")
            return response
        except Exception as e:
            # Log exception details
            logging.error(f"Unhandled error: {e}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )

app.add_middleware(LogMiddleware)