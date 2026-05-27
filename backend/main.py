import os
import uuid
from contextlib import asynccontextmanager
from datetime import date

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import date as date_type

from sqlalchemy.orm import Session, selectinload

import models, schemas
from database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas / verificadas correctamente")
    except Exception as e:
        print(f"❌ Error al conectar con la base de datos: {e}")
    yield


app = FastAPI(
    title="Dog Bar Meraki — API",
    description="Sistema de registro de animales para Dog Bar Meraki",
    version="1.2.0",
    lifespan=lifespan,
)

_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
_origins = ["*"] if _origins_env == "*" else [o.strip() for o in _origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _auto_doc_id() -> str:
    return f"ANON-{uuid.uuid4().hex[:8].upper()}"


# ─────────────────────────────────────────────
# Propietarios
# ─────────────────────────────────────────────

@app.post("/owners", response_model=schemas.OwnerOut, status_code=status.HTTP_201_CREATED, tags=["Propietarios"])
def create_owner(body: schemas.OwnerCreate, db: Session = Depends(get_db)):
    doc_id = (body.document_id or "").strip() or _auto_doc_id()
    existing = db.query(models.Owner).filter(models.Owner.document_id == doc_id).first()
    if existing:
        return existing
    data = body.model_dump()
    data["document_id"] = doc_id
    owner = models.Owner(**data)
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return owner


@app.patch("/owners/{owner_id}", response_model=schemas.OwnerOut, tags=["Propietarios"])
def update_owner(owner_id: int, body: schemas.OwnerUpdate, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(owner, k, v)
    db.commit()
    db.refresh(owner)
    return owner


@app.get("/owners", response_model=list[schemas.OwnerOut], tags=["Propietarios"])
def list_owners(db: Session = Depends(get_db)):
    return db.query(models.Owner).all()


@app.get("/owners/{owner_id}", response_model=schemas.OwnerOut, tags=["Propietarios"])
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.get(models.Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    return owner


# ─────────────────────────────────────────────
# Animales
# ─────────────────────────────────────────────

@app.post("/animals", response_model=schemas.AnimalOut, status_code=status.HTTP_201_CREATED, tags=["Animales"])
def create_animal(body: schemas.AnimalCreate, db: Session = Depends(get_db)):
    if not db.get(models.Owner, body.owner_id):
        raise HTTPException(status_code=404, detail="Propietario no encontrado")
    animal = models.Animal(**body.model_dump())
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal


@app.patch("/animals/{animal_id}", response_model=schemas.AnimalOut, tags=["Animales"])
def update_animal(animal_id: int, body: schemas.AnimalUpdate, db: Session = Depends(get_db)):
    animal = db.get(models.Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(animal, k, v)
    db.commit()
    db.refresh(animal)
    return animal


@app.get("/animals/search", response_model=list[schemas.AnimalOut], tags=["Animales"])
def search_animals(name: str = "", db: Session = Depends(get_db)):
    q = db.query(models.Animal)
    if name:
        q = q.filter(models.Animal.name.ilike(f"%{name}%"))
    return q.order_by(models.Animal.name).limit(20).all()


@app.get("/animals", response_model=list[schemas.AnimalOut], tags=["Animales"])
def list_animals(db: Session = Depends(get_db)):
    return db.query(models.Animal).all()


@app.get("/animals/{animal_id}", response_model=schemas.AnimalWithHistory, tags=["Animales"])
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal)\
        .options(
            selectinload(models.Animal.owner),
            selectinload(models.Animal.visits),
        )\
        .filter(models.Animal.id == animal_id)\
        .first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    return animal


# ─────────────────────────────────────────────
# Visitas
# ─────────────────────────────────────────────

@app.post("/visits", response_model=schemas.VisitOut, status_code=status.HTTP_201_CREATED, tags=["Visitas"])
def create_visit(body: schemas.VisitCreate, db: Session = Depends(get_db)):
    if not db.get(models.Animal, body.animal_id):
        raise HTTPException(status_code=404, detail="Animal no encontrado")
    visit = models.Visit(**body.model_dump())
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@app.get("/visits/today", response_model=list[schemas.VisitFull], tags=["Visitas"])
def visits_today(local_date: date_type | None = None, db: Session = Depends(get_db)):
    # El frontend envía la fecha local del navegador para evitar desfase UTC vs España
    today = local_date or date_type.today()
    return db.query(models.Visit)\
        .options(
            selectinload(models.Visit.animal).selectinload(models.Animal.owner)
        )\
        .filter(models.Visit.entry_date == today)\
        .order_by(models.Visit.entry_time.desc())\
        .all()


@app.get("/visits", response_model=list[schemas.VisitOut], tags=["Visitas"])
def list_visits(db: Session = Depends(get_db)):
    return db.query(models.Visit)\
        .order_by(models.Visit.entry_date.desc(), models.Visit.entry_time.desc()).all()
