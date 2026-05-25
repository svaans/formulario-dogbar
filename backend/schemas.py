from datetime import date, time
from pydantic import BaseModel, Field


# ── Owner ──────────────────────────────────────────────────────────────────────

class OwnerCreate(BaseModel):
    full_name: str | None = None
    document_id: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class OwnerOut(BaseModel):
    id: int
    full_name: str | None = None
    document_id: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    model_config = {"from_attributes": True}


class OwnerUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None


# ── Animal ─────────────────────────────────────────────────────────────────────

class AnimalCreate(BaseModel):
    owner_id: int
    name: str | None = None
    species: str | None = Field(None, pattern="^(perro|gato|otro)$")
    breed: str | None = None
    sex: str | None = Field(None, pattern="^(macho|hembra|desconocido)$")
    birth_date: date | None = None
    weight_kg: float | None = None
    size: str | None = Field(None, pattern="^(pequeño|mediano|grande)$")
    color: str | None = None
    is_vaccinated: bool = False
    rabies_up_to_date: bool = False
    last_vaccination_date: date | None = None
    is_dewormed: bool = False
    has_microchip: bool = False
    microchip_number: str | None = None
    sociability_level: str | None = Field(None, pattern="^(bajo|medio|alto)$")
    aggressive_with_animals: bool = False
    aggressive_with_humans: bool = False
    behavior_notes: str | None = None


class AnimalUpdate(BaseModel):
    name: str | None = None
    species: str | None = Field(None, pattern="^(perro|gato|otro)$")
    breed: str | None = None
    sex: str | None = Field(None, pattern="^(macho|hembra|desconocido)$")
    birth_date: date | None = None
    weight_kg: float | None = None
    size: str | None = Field(None, pattern="^(pequeño|mediano|grande)$")
    color: str | None = None
    is_vaccinated: bool | None = None
    rabies_up_to_date: bool | None = None
    last_vaccination_date: date | None = None
    is_dewormed: bool | None = None
    has_microchip: bool | None = None
    microchip_number: str | None = None
    sociability_level: str | None = Field(None, pattern="^(bajo|medio|alto)$")
    aggressive_with_animals: bool | None = None
    aggressive_with_humans: bool | None = None
    behavior_notes: str | None = None


class AnimalOut(AnimalCreate):
    id: int
    model_config = {"from_attributes": True}


class AnimalBrief(BaseModel):
    id: int
    name: str | None = None
    species: str | None = None
    breed: str | None = None
    color: str | None = None
    size: str | None = None
    aggressive_with_animals: bool = False
    aggressive_with_humans: bool = False
    sociability_level: str | None = None
    owner: OwnerOut
    model_config = {"from_attributes": True}


class AnimalWithHistory(AnimalOut):
    owner: OwnerOut
    visits: list["VisitOut"] = []


# ── Visit ──────────────────────────────────────────────────────────────────────

class VisitCreate(BaseModel):
    animal_id: int
    entry_date: date
    entry_time: time
    table_number: str | None = None
    staff_notes: str | None = None
    accepted_terms: bool = False


class VisitOut(VisitCreate):
    id: int
    model_config = {"from_attributes": True}


class VisitFull(BaseModel):
    id: int
    entry_date: date
    entry_time: time
    table_number: str | None = None
    staff_notes: str | None = None
    accepted_terms: bool = False
    animal: AnimalBrief
    model_config = {"from_attributes": True}


AnimalWithHistory.model_rebuild()
