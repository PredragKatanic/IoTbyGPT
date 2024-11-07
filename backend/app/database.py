from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Kreiranje engine za povezivanje sa bazom podataka
engine = create_engine(settings.database_url)

# Kreiranje SQLAlchemy sesije
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Osnovni model za SQLAlchemy
Base = declarative_base()

# Funkcija za dobijanje sesije baze
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
