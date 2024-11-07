from fastapi import FastAPI
from app.database import Base, engine
from app.routes import measurement_router  # koristi measurement_router iz __init__.py
from fastapi.middleware.cors import CORSMiddleware

# Inicijalizacija baze podataka
Base.metadata.create_all(bind=engine)

# Kreiranje instance FastAPI aplikacije
app = FastAPI()

# Definišite dozvoljene izvore (origins) za CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8080",
    # Dodajte druge dozvoljene URL-ove ako je potrebno
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Dozvoljeni izvori
    allow_credentials=True,
    allow_methods=["*"],              # Dozvoljeni HTTP metodi (GET, POST, itd.)
    allow_headers=["*"],              # Dozvoljeni HTTP zaglavlja
)

# Primer osnovne rute za proveru rada aplikacije
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

# Učitaj rute za measurement
app.include_router(measurement_router, prefix="/api")