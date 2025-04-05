from fastapi import Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from src.app.services.ServiceFactory import ServiceFactory
from src.app.models.UploadModel import Upload
from src.app.config.database import get_db
import shutil
import os
import json
from datetime import datetime


class DetectionController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DetectionController, cls).__new__(cls)
            cls._instance.upload_dir = "uploads"
            os.makedirs(f"{cls._instance.upload_dir}/original", exist_ok=True)
            os.makedirs(f"{cls._instance.upload_dir}/detected", exist_ok=True)
        return cls._instance

    async def detect_pests(
        self,
        file: UploadFile = File(...),
        model_version: str = Query("v1", description="Model version to use (v1 or v2)"),
        db: Session = Depends(get_db),
    ):

        detection_service = ServiceFactory.create_detection_service(
            "yolo", model_version
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = f"{self.upload_dir}/original/{timestamp}_{file.filename}"
        detected_filename = f"{self.upload_dir}/detected/{timestamp}_{file.filename}"

        try:
            with open(original_filename, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to save original file: {str(e)}"
            )

        try:
            detection_result = detection_service.detect_pests(
                original_filename, detected_filename
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")

        upload = Upload(
            original_image=original_filename,
            detected_image=detected_filename,
            detection_result=json.dumps(detection_result),
        )
        db.add(upload)
        db.commit()
        db.refresh(upload)

        return {
            "upload_id": upload.id,
            "original_image": original_filename,
            "detected_image": detected_filename,
            "detection_result": detection_result,
            "model_version": model_version,
            "created_at": upload.created_at.isoformat(),
        }

    async def get_history(
        self, db: Session = Depends(get_db), page: int = 1, limit: int = 10
    ):
        offset = (page - 1) * limit
        total = db.query(Upload).count()
        uploads = db.query(Upload).offset(offset).limit(limit).all()

        return {
            "data": [
                {
                    "id": u.id,
                    "original": u.original_image,
                    "detected": u.detected_image,
                    "result": json.loads(u.detection_result),
                    "created_at": u.created_at.isoformat(),
                }
                for u in uploads
            ],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit,
            },
        }

    async def get_detection(self, upload_id: int, db: Session = Depends(get_db)):
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Detection not found")
        return {
            "id": upload.id,
            "original": upload.original_image,
            "detected": upload.detected_image,
            "result": json.loads(upload.detection_result),
            "created_at": upload.created_at.isoformat(),
        }

    async def delete_detection(self, upload_id: int, db: Session = Depends(get_db)):
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if not upload:
            raise HTTPException(status_code=404, detail="Detection not found")

        try:
            if os.path.exists(upload.original_image):
                os.remove(upload.original_image)
            if os.path.exists(upload.detected_image):
                os.remove(upload.detected_image)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to delete files: {str(e)}"
            )

        db.delete(upload)
        db.commit()
        return {"message": f"Detection {upload_id} deleted successfully"}
