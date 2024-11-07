from pydantic import BaseModel
from datetime import datetime

class MeasurementBase(BaseModel):
    temperature: float
    humidity: float

class MeasurementCreate(MeasurementBase):
    pass

class MeasurementResponse(MeasurementBase):
    id: int
    measurement_time: datetime

    class Config:
        orm_mode = True
