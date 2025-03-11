from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from internal.api.login import router as login_router
from internal.api.service_status import router as service_status_router
from internal.api.user import router as user_router
from internal.api.token import router as token_router
from internal.api.exception_handlers import generic_exception_handler, validation_exception_handler
from config.config import get_config, set_config
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(login_router, prefix=get_config("api_prefix"), tags=["Authenticate and Session Management"])
app.include_router(token_router, prefix=get_config("api_prefix"), tags=["Token Management"])
app.include_router(user_router, prefix=get_config("api_prefix"), tags=["User Management"])
app.include_router(service_status_router, prefix=get_config("api_prefix"), tags=["Service Status"])

# Exception handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    set_config("health", True)
    set_config("ready", True)

    uvicorn.run(app, host="0.0.0.0", port=get_config("api_port"))


