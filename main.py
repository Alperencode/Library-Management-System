from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from internal.utils.logger import logger
from internal.database.database import check_connection, client
from internal.api.exception_handlers import generic_exception_handler, validation_exception_handler
from internal.api import book, user, login, token, service_status, google_books, user_book_operations
from config.config import get_config, set_config
import uvicorn
import sys


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await check_connection()
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Failed to connect to the database. Details: {e}")
        sys.exit(1)

    # Let FastAPI start serving requests
    yield

    # Shutdown
    client.close()
    logger.info("Database connection closed.")


app = FastAPI(lifespan=lifespan)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081", "http://localhost:8082"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(login.router, prefix=get_config("api_prefix"), tags=["Authenticate and Session Management"])
app.include_router(token.router, prefix=get_config("api_prefix"), tags=["Token Management"])
app.include_router(user.router, prefix=get_config("api_prefix"), tags=["User Management"])
app.include_router(service_status.router, prefix=get_config("api_prefix"), tags=["Service Status"])
app.include_router(book.router, prefix=get_config("api_prefix"), tags=["Book Management"])
app.include_router(google_books.router, prefix=get_config("api_prefix"), tags=["Google Books"])
app.include_router(user_book_operations.router, prefix=get_config("api_prefix"), tags=["User Book Operations"])

# Exception handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    set_config("health", True)
    set_config("ready", True)

    uvicorn.run(app, host="0.0.0.0", port=get_config("api_port"))
