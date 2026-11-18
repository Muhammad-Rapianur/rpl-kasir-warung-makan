"""Uji Langkah 9 Jobsheet 11: Pembuktian Validasi Dua Lapis (Bypass Klien ditolak Server)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app

client = app.app.test_client()

# Login terlebih dahulu sebagai pemilik
client.post("/login", data={"username": "pak_joko", "password": "joko12345"})

print("=== UJI LANGKAH 9: VALIDASI DUA LAPIS (KLIEN & SERVER) ===")

# Simulasi bypass klien: Mengirim input yang melanggar atribut HTML5 via HTTP POST langsung
res_bypass1 = client.post(
    "/menu/tambah",
    data={"nama": "", "kategori_id": "1", "harga": "15000"},
)
assert res_bypass1.status_code == 200
assert "Nama menu hidangan wajib diisi." in res_bypass1.get_data(as_text=True)
print("  [LULUS] Skenario 1: Bypass required nama ditolak oleh validasi server.")

res_bypass2 = client.post(
    "/menu/tambah",
    data={"nama": "Bebek Goreng Spesial", "kategori_id": "1", "harga": "-10000"},
)
assert res_bypass2.status_code == 200
assert "Harga jual harus berupa bilangan bulat positif" in res_bypass2.get_data(as_text=True)
print("  [LULUS] Skenario 2: Bypass min='1' (harga negatif) ditolak oleh server.")

res_bypass3 = client.post(
    "/menu/tambah",
    data={"nama": "Bebek Goreng Spesial", "kategori_id": "1", "harga": "bukan_angka"},
)
assert res_bypass3.status_code == 200
assert "Harga jual harus berupa bilangan bulat positif" in res_bypass3.get_data(as_text=True)
print("  [LULUS] Skenario 3: Bypass type='number' (string teks) ditolak oleh server.")

print(">>> SELURUH UJI VALIDASI DUA LAPIS LULUS 100% <<<")
