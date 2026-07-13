from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class SettingsBase(BaseModel):
    confidence_threshold: float
    nms_threshold: float
    alert_sound: bool
    dark_mode: bool
    model_name: str
    twilio_sid: Optional[str] = ""
    twilio_token: Optional[str] = ""
    twilio_from: Optional[str] = ""
    twilio_to: Optional[str] = ""
    twilio_enabled: bool

class SettingsUpdate(BaseModel):
    confidence_threshold: Optional[float] = None
    nms_threshold: Optional[float] = None
    alert_sound: Optional[bool] = None
    dark_mode: Optional[bool] = None
    model_name: Optional[str] = None
    twilio_sid: Optional[str] = None
    twilio_token: Optional[str] = None
    twilio_from: Optional[str] = None
    twilio_to: Optional[str] = None
    twilio_enabled: Optional[bool] = None

class SettingsResponse(SettingsBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class DetectionHistoryResponse(BaseModel):
    id: int
    timestamp: datetime
    vehicle_count: int
    car_count: int
    bus_count: int
    truck_count: int
    motorcycle_count: int
    accident_detected: bool
    confidence: float
    source: str
    image_path: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class StatsResponse(BaseModel):
    total_vehicles: int
    total_accidents: int
    detection_accuracy: float
    today_alerts: int
    fps: float
    model_name: str
    confidence_threshold: float
    nms_threshold: float

class SystemHealth(BaseModel):
    cpu_usage: float
    ram_usage: float
    latency_ms: float
    database_status: str
    gpu_available: bool
