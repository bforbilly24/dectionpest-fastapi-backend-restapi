from fastapi import APIRouter, Depends
from src.app.controllers.api.DetectionController import DetectionController

router = APIRouter(prefix="/v1")

detection_controller = DetectionController()

router.post("/detect")(detection_controller.detect_pests)
router.get("/history")(detection_controller.get_history)
router.get("/detect/{upload_id}")(detection_controller.get_detection)
router.delete("/detect/{upload_id}")(detection_controller.delete_detection)
