from fastapi import FastAPI
from src.app.routes.v1 import router
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os

load_dotenv()

app = FastAPI(
    title="Pest Detection API",
    description="API for detecting pest diseases using YOLO v8",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Pest Detection API is running!"}

# Mount the router - this was missing!
app.include_router(router, prefix="/api")

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")