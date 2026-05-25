-- Dog Bar Meraki — Schema de base de datos
-- Compatible con SQLite y PostgreSQL

PRAGMA foreign_keys = ON;

-- ─────────────────────────────────────────────
-- Propietarios
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS owners (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name   TEXT    NOT NULL,
    document_id TEXT    NOT NULL UNIQUE,   -- DNI / NIE / Pasaporte
    phone       TEXT    NOT NULL,
    email       TEXT,
    address     TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- Animales
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS animals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id    INTEGER NOT NULL REFERENCES owners(id) ON DELETE CASCADE,

    -- Datos básicos
    name        TEXT    NOT NULL,
    species     TEXT    NOT NULL CHECK(species IN ('perro','gato','otro')),
    breed       TEXT,
    sex         TEXT    CHECK(sex IN ('macho','hembra','desconocido')),
    birth_date  DATE,
    weight_kg   REAL,
    size        TEXT    CHECK(size IN ('pequeño','mediano','grande')),
    color       TEXT,

    -- Información sanitaria
    is_vaccinated          INTEGER DEFAULT 0 CHECK(is_vaccinated IN (0,1)),
    rabies_up_to_date      INTEGER DEFAULT 0 CHECK(rabies_up_to_date IN (0,1)),
    last_vaccination_date  DATE,
    is_dewormed            INTEGER DEFAULT 0 CHECK(is_dewormed IN (0,1)),
    has_microchip          INTEGER DEFAULT 0 CHECK(has_microchip IN (0,1)),
    microchip_number       TEXT,

    -- Comportamiento
    sociability_level          TEXT CHECK(sociability_level IN ('bajo','medio','alto')),
    aggressive_with_animals    INTEGER DEFAULT 0 CHECK(aggressive_with_animals IN (0,1)),
    aggressive_with_humans     INTEGER DEFAULT 0 CHECK(aggressive_with_humans IN (0,1)),
    behavior_notes             TEXT,

    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- Visitas
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS visits (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id       INTEGER NOT NULL REFERENCES animals(id) ON DELETE CASCADE,

    entry_date      DATE     NOT NULL DEFAULT (DATE('now')),
    entry_time      TIME     NOT NULL DEFAULT (TIME('now')),
    table_number    TEXT,
    staff_notes     TEXT,
    accepted_terms  INTEGER  NOT NULL DEFAULT 0 CHECK(accepted_terms IN (0,1)),

    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────────
-- Índices para consultas frecuentes
-- ─────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_animals_owner   ON animals(owner_id);
CREATE INDEX IF NOT EXISTS idx_visits_animal   ON visits(animal_id);
CREATE INDEX IF NOT EXISTS idx_visits_date     ON visits(entry_date);
CREATE INDEX IF NOT EXISTS idx_owners_doc      ON owners(document_id);
