from src.app.services.DetectionService import DetectionService


class ServiceFactory:
    _instances = {}
    MODEL_PATHS = {
        "v1": "src/ml_models/best.pt",
    }
    DEFAULT_MODEL_VERSION = "v1"

    @staticmethod
    def create_detection_service(
        service_type: str = "yolo", model_version: str = None
    ) -> DetectionService:
        model_version = model_version or ServiceFactory.DEFAULT_MODEL_VERSION
        if model_version not in ServiceFactory.MODEL_PATHS:
            raise ValueError(
                f"Unknown model version: {model_version}. Only 'v1' is available."
            )

        model_path = ServiceFactory.MODEL_PATHS[model_version]
        key = (service_type, model_path)

        if key not in ServiceFactory._instances:
            if service_type.lower() == "yolo":
                ServiceFactory._instances[key] = DetectionService(model_path)
            else:
                raise ValueError(f"Unknown detection service type: {service_type}")

        return ServiceFactory._instances[key]