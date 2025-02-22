from fastapi import FastAPI
from internal.api.login import router as login_router

app = FastAPI()

app.include_router(login_router, prefix="/api/v1", tags=["Authenticate and Session Management"])
