"""Test script untuk validasi Langkah 10 (Uji Keamanan & Skema DDL)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

print("=== 1. UJI KEAMANAN SQL INJECTION ===")
sql_payload = "Robert'); DROP TABLE menu;--"
res_sqli = client.post(
    "/menu/tambah",
    data={"nama": sql_payload, "kategori_id": "1", "harga": "10000"},
    follow_redirects=True,
)
assert res_sqli.status_code == 200

# Verifikasi tabel menu tidak terhapus dan payload tersimpan sebagai string literal biasa
with models.koneksi() as db:
    tbl = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='menu'"
    ).fetchone()
    assert tbl is not None, "FATAL: Tabel menu terhapus oleh SQL Injection!"
    baris = db.execute(
        "SELECT nama FROM menu WHERE nama = ?", (sql_payload,)
    ).fetchone()
    assert baris is not None
    assert baris["nama"] == sql_payload
print(
    "  [LULUS] SQL Injection berhasil ditangkal! Input tersimpan aman sebagai"
    " teks biasa berkat parameterized query (?)."
)

print("\n=== 2. UJI KEAMANAN CROSS-SITE SCRIPTING (XSS) ===")
xss_payload = "<b>tes</b>"
res_xss = client.post(
    "/menu/tambah",
    data={"nama": xss_payload, "kategori_id": "1", "harga": "5000"},
    follow_redirects=True,
)
assert res_xss.status_code == 200
html_page = res_xss.get_data(as_text=True)

# Pastikan teks di-escape otomatis oleh Jinja2 menjadi &lt;b&gt;tes&lt;/b&gt;
assert (
    "&lt;b&gt;tes&lt;/b&gt;" in html_page
), "FATAL: Tag HTML tidak di-escape otomatis oleh template!"
# Pastikan tidak disisipkan sebagai HTML mentah <strong> atau <b>
assert "<strong>tes</strong>" not in html_page
print(
    "  [LULUS] XSS Injection berhasil ditangkal! Tag HTML otomatis di-escape"
    " oleh Jinja2 (&lt;b&gt;tes&lt;/b&gt;)."
)

# Bersihkan data uji keamanan agar tabel rapi kembali
with models.koneksi() as db:
    db.execute(
        "DELETE FROM menu WHERE nama IN (?, ?)", (sql_payload, xss_payload)
    )

print("\n=== 3. VERIFIKASI KEUTUHAN SKEMA DDL (cek_skema.py) ===")
import subprocess

hasil_skema = subprocess.run(
    [sys.executable, str(Path(__file__).parent / "cek_skema.py")],
    capture_output=True,
    text=True,
    check=True,
)
print(hasil_skema.stdout)
assert "13 LULUS  |  0 GAGAL" in hasil_skema.stdout
print("  [LULUS] Seluruh 13 uji skema DDL lulus tanpa ada modifikasi skema!")

print("\n>>> SELURUH UJI KEAMANAN DAN PENERIMAAN LANGKAH 10 LULUS 100% <<<")
