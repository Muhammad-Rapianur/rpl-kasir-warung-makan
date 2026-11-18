import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Jalur berkas basis data SQLite dan skema DDL
DB_PATH = Path(__file__).with_name("kasir_warung.db")
SCHEMA_PATH = Path(__file__).parent / "docs" / "desain" / "schema.sql"


@contextmanager
def koneksi():
    """Buka koneksi SQLite, aktifkan kunci asing (foreign keys),

    gunakan row_factory Row, lalu commit dan tutup secara aman.
    """
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def init_db():
    """Inisialisasi basis data dari schema.sql jika kasir_warung.db belum ada."""
    if not DB_PATH.exists():
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Berkas skema tidak ditemukan di {SCHEMA_PATH}")
        with koneksi() as db:
            db.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
