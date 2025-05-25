import uvicorn
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from config.config import get_config, set_config, LOCAL_IP
from internal.utils.logger import logger
from internal.database.database import check_connection, client
from internal.api.utils.exception_handlers import generic_exception_handler, validation_exception_handler
from internal.cron_jobs.penalty_handler import start_cron_jobs, check_penalties
from internal.api.auth import login, token
from internal.api.book import books, google_books, request_book, user_book_operations
from internal.api.user import user, reset_password
from internal.api.utils import service_status
from internal.api.admin import (
    admin_auth, admin_dashboard,
    admin_request_management, admin_user_management,
    admin_borrow_management, admin_book_management
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await check_connection()
        logger.info("Successfully connected to the database.")

        start_cron_jobs()
        logger.info("Successfully started the cron jobs.")

        await check_penalties()
        logger.info("Successfully checked penalties.")
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
    allow_origins=["http://localhost:8085", f"http://{LOCAL_IP}:8085"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(login.router, prefix=get_config("api_prefix"), tags=["Authenticate and Session Management"])
app.include_router(token.router, prefix=get_config("api_prefix"), tags=["Token Management"])
app.include_router(user.router, prefix=get_config("api_prefix"), tags=["User Management"])
app.include_router(reset_password.router, prefix=get_config("api_prefix"), tags=["Reset Password"])
app.include_router(service_status.router, prefix=get_config("api_prefix"), tags=["Service Status"])
app.include_router(books.router, prefix=get_config("api_prefix"), tags=["Book Management"])
app.include_router(google_books.router, prefix=get_config("api_prefix"), tags=["Google Books"])
app.include_router(user_book_operations.router, prefix=get_config("api_prefix"), tags=["User Book Operations"])
app.include_router(request_book.router, prefix=get_config("api_prefix"), tags=["Request Book Operations"])
app.include_router(admin_auth.router, prefix=get_config("api_prefix"), tags=["Admin Management"])
app.include_router(admin_dashboard.router, prefix=get_config("api_prefix"), tags=["Admin Dashboard Management"])
app.include_router(admin_user_management.router, prefix=get_config("api_prefix"), tags=["Admin Operations"])
app.include_router(admin_request_management.router, prefix=get_config("api_prefix"), tags=["Admin Request Management"])
app.include_router(admin_borrow_management.router, prefix=get_config("api_prefix"), tags=["Admin Borrow Management"])
app.include_router(admin_book_management.router, prefix=get_config("api_prefix"), tags=["Admin Book Management"])

# Exception handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    set_config("health", True)
    set_config("ready", True)

    uvicorn.run(app, host=LOCAL_IP, port=get_config("api_port"))
