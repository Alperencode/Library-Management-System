from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from internal.api.login import router as login_router
from internal.api.exception_handlers import generic_exception_handler, validation_exception_handler

app = FastAPI()

# Routers
app.include_router(login_router, prefix="/api/v1", tags=["Authenticate and Session Management"])

# Exception handlers
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
