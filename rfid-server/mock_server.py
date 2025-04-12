import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import LOCAL_IP
from internal.api import mock_read_write


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8085", f"http://{LOCAL_IP}:8085"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mock_read_write.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host=LOCAL_IP, port=8001)
