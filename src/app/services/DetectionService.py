# src/app/services/DetectionService.py
from ultralytics import YOLO
import cv2


class DetectionService:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)
        self.class_names = self.model.names

    def detect_pests(self, image_path: str, output_path: str) -> dict:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at {image_path}")

        results = self.model.predict(
            source=image, save=False, show=False, conf=0.5, iou=0.4
        )

        detection_data = {
            "grasshopper_bites": 0,
            "caterpillar_bites": 0,
            "detections": [],
        }

        for result in results:
            boxes = result.boxes.xyxy
            confs = result.boxes.conf
            classes = result.boxes.cls

            for box, conf, cls in zip(boxes, confs, classes):
                x1, y1, x2, y2 = map(int, box)
                class_name = self.class_names[int(cls)]
                label = f"{class_name}: {conf:.2f}"

                if "grasshopper" in class_name.lower():
                    detection_data["grasshopper_bites"] += 1
                elif "caterpillar" in class_name.lower():
                    detection_data["caterpillar_bites"] += 1

                detection_data["detections"].append(
                    {
                        "class": class_name,
                        "confidence": float(conf),
                        "box": [x1, y1, x2, y2],
                    }
                )

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    image,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

        cv2.imwrite(output_path, image)
        return detection_data
