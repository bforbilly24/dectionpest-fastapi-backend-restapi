from fastapi import FastAPI
from src.app.routes import v1
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Dental Disease Detection API",
    description="API for detecting dental diseases using YOLO v8",
    version="1.0.0",
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(v1.router, prefix="/api")

from fastapi import FastAPI
from src.app.routes.v1 import router
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os

load_dotenv()

app = FastAPI(
    title="Pest Detection API",
    description="API for detecting dental diseases using YOLO v8",
    version="1.0.0",
)
@app.get("/")
async def root():
    return {"message": "Pest Detection API is running!"}

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

