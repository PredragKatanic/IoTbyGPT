from sqlalchemy import Column, Integer, TIMESTAMP, DECIMAL
from app.database import Base

class Measurement(Base):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True)
    measurement_time = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    temperature = Column(DECIMAL(5, 2))
    humidity = Column(DECIMAL(5, 2))

