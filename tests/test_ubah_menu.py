"""Test script untuk validasi Langkah 8 (Ubah Menu)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

# 1. Test GET /menu/1/ubah (data lama terisi)
res_get = client.get("/menu/1/ubah")
assert res_get.status_code == 200
html_get = res_get.get_data(as_text=True)
assert "Ubah Menu Hidangan" in html_get
assert "Nasi Putih" in html_get
print("  [LULUS] Uji 1: Form ubah terisi data lama (nama, harga, kategori).")

# 2. Test POST ubah menu valid (harga diubah ke 5000 dan status ke 'habis')
res_ubah = client.post(
    "/menu/1/ubah",
    data={
        "nama": "Nasi Putih Pulen",
        "kategori_id": "1",
        "harga": "5000",
        "status": "habis",
    },
    follow_redirects=True,
)
assert res_ubah.status_code == 200
html_ubah = res_ubah.get_data(as_text=True)
assert "Nasi Putih Pulen" in html_ubah
assert "Rp 5.000" in html_ubah
assert "Habis" in html_ubah
print("  [LULUS] Uji 2: Ubah menu berhasil & perubahan terlihat di daftar.")

# 3. Test POST nama duplikat (mengubah jadi nama yang sudah dipakai menu lain)
res_duplikat = client.post(
    "/menu/1/ubah",
    data={
        "nama": "Ayam Goreng",
        "kategori_id": "1",
        "harga": "5000",
        "status": "tersedia",
    },
)
assert res_duplikat.status_code == 200
html_dup = res_duplikat.get_data(as_text=True)
assert "sudah terdaftar" in html_dup
print("  [LULUS] Uji 3: Mengubah menjadi nama yang sudah ada ditolak (IntegrityError).")

# 4. Test ID 999 (tidak ada) menghasilkan 404
res_404 = client.get("/menu/999/ubah")
assert res_404.status_code == 404
print("  [LULUS] Uji 4: Membuka menu/999/ubah menghasilkan 404 Not Found.")

print("\n>>> SELURUH UJI LANGKAH 8 LULUS 100% <<<")
