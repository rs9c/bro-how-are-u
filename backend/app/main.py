from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ping, stream

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5501", "http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(ping.router)
app.include_router(stream.router)


@app.get("/")
async def root():
    return {"msg": "Hello world! Running on port 5502"}
