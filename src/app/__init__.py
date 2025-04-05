from fastapi import FastAPI
from src.app.routes import v1

app = FastAPI(
    title="Dental Disease Detection API",
    description="API for detecting dental diseases using YOLO v8",
    version="1.0.0",
)

app.include_router(v1.router, prefix="/api")
