from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from datetime import datetime
from .database import Base, engine

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    confidence_threshold = Column(Float, default=0.5)
    nms_threshold = Column(Float, default=0.4)
    alert_sound = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=True)
    model_name = Column(String, default="yolov4-tiny")
    
    # Twilio Integration Settings
    twilio_sid = Column(String, default="", nullable=True)
    twilio_token = Column(String, default="", nullable=True)
    twilio_from = Column(String, default="", nullable=True)
    twilio_to = Column(String, default="", nullable=True)
    twilio_enabled = Column(Boolean, default=False)

class DetectionHistory(Base):
    __tablename__ = "detection_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    vehicle_count = Column(Integer, default=0)
    car_count = Column(Integer, default=0)
    bus_count = Column(Integer, default=0)
    truck_count = Column(Integer, default=0)
    motorcycle_count = Column(Integer, default=0)
    accident_detected = Column(Boolean, default=False)
    confidence = Column(Float, default=0.0)
    source = Column(String, default="Upload Video")  # "Upload Video" or "Live Webcam"
    image_path = Column(String, nullable=True)  # Path to the saved detection screenshot

# Create tables
Base.metadata.create_all(bind=engine)
