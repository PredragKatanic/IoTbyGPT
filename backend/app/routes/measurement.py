from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementCreate, MeasurementResponse

router = APIRouter()

# Ruta za dodavanje novog merenja
@router.post("/measurements/", response_model=MeasurementResponse)
def create_measurement(measurement: MeasurementCreate, db: Session = Depends(get_db)):
    db_measurement = Measurement(
        temperature=measurement.temperature,
        humidity=measurement.humidity
    )
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

# Ruta za preuzimanje poslednjeg merenja
@router.get("/measurements/latest", response_model=MeasurementResponse)
def get_latest_measurement(db: Session = Depends(get_db)):
    measurement = db.query(Measurement).order_by(Measurement.measurement_time.desc()).first()
    if not measurement:
        raise HTTPException(status_code=404, detail="Measurement not found")
    return measurement

# Ruta za preuzimanje poslednjih 300 merenja (5 minuta x 60 sekundi)
@router.get("/measurements/", response_model=List[MeasurementResponse])
def get_measurements(db: Session = Depends(get_db)):
    measurements = db.query(Measurement).order_by(Measurement.measurement_time.desc()).limit(300).all()
    return measurements
