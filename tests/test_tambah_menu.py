"""Test script untuk validasi Langkah 6 (Tambah Menu)."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

# Uji 1: Semua kolom valid
res1 = client.post(
    "/menu/tambah",
    data={"nama": "Bebek Goreng", "kategori_id": "2", "harga": "25000"},
    follow_redirects=True,
)
assert res1.status_code == 200
html1 = res1.get_data(as_text=True)
assert "Bebek Goreng" in html1
assert "Rp 25.000" in html1
print("  [LULUS] Uji 1: Menu valid berhasil disimpan & tampil di tabel.")

# Uji 2: Nama kosong
res2 = client.post(
    "/menu/tambah",
    data={"nama": "", "kategori_id": "2", "harga": "25000"},
)
assert res2.status_code == 200
html2 = res2.get_data(as_text=True)
assert "Nama menu hidangan wajib diisi" in html2
print("  [LULUS] Uji 2: Nama kosong ditolak dengan pesan galat.")

# Uji 3: Harga negatif (-5)
res3 = client.post(
    "/menu/tambah",
    data={"nama": "Menu Negatif", "kategori_id": "2", "harga": "-5"},
)
assert res3.status_code == 200
html3 = res3.get_data(as_text=True)
assert "Harga jual harus berupa bilangan bulat positif" in html3
print("  [LULUS] Uji 3: Harga negatif ditolak dengan pesan galat.")

# Uji 4: Harga teks non-angka ('abc')
res4 = client.post(
    "/menu/tambah",
    data={"nama": "Menu Huruf", "kategori_id": "2", "harga": "abc"},
)
assert res4.status_code == 200
html4 = res4.get_data(as_text=True)
assert "Harga jual harus berupa bilangan bulat positif" in html4
print("  [LULUS] Uji 4: Harga non-angka ditolak dengan pesan galat.")

# Uji 5: Nama sudah ada (duplikat UNIQUE)
res5 = client.post(
    "/menu/tambah",
    data={"nama": "Ayam Goreng", "kategori_id": "2", "harga": "15000"},
)
assert res5.status_code == 200
html5 = res5.get_data(as_text=True)
assert "sudah terdaftar" in html5
print("  [LULUS] Uji 5: Nama duplikat ditolak dengan pesan sudah terdaftar.")

print("\n>>> SELURUH 5 SKENARIO MASUKAN LANGKAH 6 LULUS (100%) <<<")
