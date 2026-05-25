from datetime import date, datetime, time
from sqlalchemy import Boolean, DateTime, Date, Float, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Owner(Base):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(200))
    document_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # auto-generado si no lo dan
    phone: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(200))
    address: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    animals: Mapped[list["Animal"]] = relationship("Animal", back_populates="owner", cascade="all, delete")


class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("owners.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str | None] = mapped_column(String(100))
    species: Mapped[str | None] = mapped_column(String(20))
    breed: Mapped[str | None] = mapped_column(String(100))
    sex: Mapped[str | None] = mapped_column(String(20))
    birth_date: Mapped[date | None] = mapped_column(Date)
    weight_kg: Mapped[float | None] = mapped_column(Float)
    size: Mapped[str | None] = mapped_column(String(20))
    color: Mapped[str | None] = mapped_column(String(100))

    is_vaccinated: Mapped[bool] = mapped_column(Boolean, default=False)
    rabies_up_to_date: Mapped[bool] = mapped_column(Boolean, default=False)
    last_vaccination_date: Mapped[date | None] = mapped_column(Date)
    is_dewormed: Mapped[bool] = mapped_column(Boolean, default=False)
    has_microchip: Mapped[bool] = mapped_column(Boolean, default=False)
    microchip_number: Mapped[str | None] = mapped_column(String(50))

    sociability_level: Mapped[str | None] = mapped_column(String(20))
    aggressive_with_animals: Mapped[bool] = mapped_column(Boolean, default=False)
    aggressive_with_humans: Mapped[bool] = mapped_column(Boolean, default=False)
    behavior_notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["Owner"] = relationship("Owner", back_populates="animals")
    visits: Mapped[list["Visit"]] = relationship("Visit", back_populates="animal", cascade="all, delete")


class Visit(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    animal_id: Mapped[int] = mapped_column(Integer, ForeignKey("animals.id", ondelete="CASCADE"), nullable=False)

    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    entry_time: Mapped[time] = mapped_column(Time, nullable=False)
    table_number: Mapped[str | None] = mapped_column(String(20))
    staff_notes: Mapped[str | None] = mapped_column(Text)
    accepted_terms: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    animal: Mapped["Animal"] = relationship("Animal", back_populates="visits")
