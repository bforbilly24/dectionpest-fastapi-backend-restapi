from sqlalchemy import Column, Integer, String, DateTime
from src.app.config.database import Base
from datetime import datetime

class Upload(Base):
    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)
    original_image = Column(String, nullable=False)
    detected_image = Column(String, nullable=False)
    detection_result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)