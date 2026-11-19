"""Fixture bersama untuk semua uji pytest.
Memakai basis data sementara, sehingga kasir_warung.db asli tidak tersentuh.
"""
import sys
import tempfile
from pathlib import Path
import pytest
from werkzeug.security import generate_password_hash

# Tambahkan direktori root proyek ke sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import models

# Tentukan basis data sementara sebelum import app
_TEMP_DIR = tempfile.mkdtemp()
models.DB_PATH = Path(_TEMP_DIR) / "uji_kasir.db"

import app as aplikasi
import percobaan
import services

SANDI_PEMILIK, SANDI_KASIR = "rahasia-uji-1", "rahasia-uji-2"


@pytest.fixture(autouse=True)
def basis_bersih():
    """Setiap uji mulai dari basis data kosong dengan dua akun uji terisolasi."""
    models.DB_PATH.unlink(missing_ok=True)
    models.init_db()
    percobaan._gagal.clear()

    # Hash cepat khusus pengujian agar 50+ uji berjalan singkat
    cepat = lambda s: generate_password_hash(s, method="pbkdf2:sha256:1000")
    models.tambah_pengguna("pak_pemilik", cepat(SANDI_PEMILIK), "Pak Pemilik Uji", "pemilik")
    models.tambah_pengguna("kasir_siti", cepat(SANDI_KASIR), "Siti Kasir Uji", "kasir")
    yield


@pytest.fixture
def kirim():
    """Fungsi pembantu POST yang otomatis menyertakan token CSRF yang sah."""
    def _kirim(c, url, ikuti=True, **data):
        with c.session_transaction() as s:
            s.setdefault("csrf_token", "token-uji-12345")
            token = s["csrf_token"]
        data.setdefault("csrf_token", token)
        return c.post(url, data=data, follow_redirects=ikuti)
    return _kirim


@pytest.fixture
def tamu():
    """Klien uji yang belum terotentikasi (tamu)."""
    return aplikasi.app.test_client()


@pytest.fixture
def pemilik(kirim):
    """Klien uji yang sudah login sebagai pemilik warung."""
    c = aplikasi.app.test_client()
    kirim(c, "/login", username="pak_pemilik", password=SANDI_PEMILIK)
    return c


@pytest.fixture
def kasir(kirim):
    """Klien uji yang sudah login sebagai kasir warung."""
    c = aplikasi.app.test_client()
    kirim(c, "/login", username="kasir_siti", password=SANDI_KASIR)
    return c
