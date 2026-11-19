"""Uji kebersihan rilis: versi, cadangan, .gitignore, changelog, dan dependensi."""
import re
import sqlite3
from pathlib import Path

import cadangkan
from versi import VERSI

AKAR = Path(__file__).resolve().parent.parent


def test_versi_berformat_semver():
    """Memastikan nomor versi mengikuti format Semantic Versioning (MAJOR.MINOR.PATCH)."""
    assert re.fullmatch(r"\d+\.\d+\.\d+", VERSI)


def test_versi_tampil_di_halaman(tamu):
    """Memastikan nomor versi tampil pada footer halaman publik / login."""
    assert f"v{VERSI}" in tamu.get("/login").text


def test_changelog_memuat_versi_rilis():
    """Memastikan berkas CHANGELOG.md memuat judul untuk versi rilis saat ini."""
    assert f"## [{VERSI}]" in (AKAR / "CHANGELOG.md").read_text(encoding="utf-8")


def test_gitignore_mengecualikan_rahasia_dan_data():
    """Memastikan berkas rahasia dan database dikecualikan oleh .gitignore."""
    baris = (AKAR / ".gitignore").read_text(encoding="utf-8").splitlines()
    for wajib in (".env", "cadangan/"):
        assert wajib in baris
    assert any("*.db" in b or "kasir_warung.db" in b for b in baris)


def test_requirements_dikunci_versinya():
    """Memastikan seluruh dependensi rilis memiliki versi yang terkunci persis (==)."""
    for baris in (AKAR / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if baris.strip() and not baris.startswith("#"):
            assert "==" in baris, f"Versi tidak dikunci pada: {baris}"


def test_cadangan_berisi_data_yang_sama(pemilik, kirim, tmp_path):
    """Memastikan fungsi cadangkan() menghasilkan salinan basis data yang valid."""
    kirim(pemilik, "/menu/tambah", nama="Ayam Uji Rilis", kategori_id="1", harga="25000")
    berkas = cadangkan.cadangkan(tmp_path)
    assert berkas.exists()
    db = sqlite3.connect(berkas)
    try:
        data = db.execute("SELECT nama, harga FROM menu WHERE nama = 'Ayam Uji Rilis'").fetchall()
        assert data == [("Ayam Uji Rilis", 25000)]
    finally:
        db.close()
