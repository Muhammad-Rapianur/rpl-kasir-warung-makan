"""Uji Langkah 5 Jobsheet 11: 4 Skenario Pembatasan Peran (Otorisasi Server)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app

client = app.app.test_client()

print("=== UJI LANGKAH 5: PEMBATASAN AKSES BERDASARKAN PERAN (403) ===")

# 1. Tamu membuka halaman utama / terlindungi
res_tamu = client.get("/menu", follow_redirects=False)
assert res_tamu.status_code == 302
assert "/login" in res_tamu.headers["Location"]
assert "next=/menu" in res_tamu.headers["Location"]
print("  [LULUS] Skenario 1: Tamu dialihkan ke halaman login dengan parameter next.")

# 2. Login sebagai kasir (siti_kasir / siti12345)
client.post("/login", data={"username": "siti_kasir", "password": "siti12345"})

# Coba buka form tambah menu (terlarang untuk kasir)
res_kasir_tambah = client.get("/menu/tambah")
assert res_kasir_tambah.status_code == 403
assert "Akses Ditolak" in res_kasir_tambah.get_data(as_text=True)
print("  [LULUS] Skenario 2: Kasir mencoba membuka /menu/tambah ditolak dengan 403 Forbidden.")

# 3. Kasir kirim aksi POST hapus menu
res_kasir_hapus = client.post("/menu/1/hapus")
assert res_kasir_hapus.status_code == 403
print("  [LULUS] Skenario 3: Kasir mengirim aksi POST hapus ditolak dengan 403 di server.")

# Keluar dari akun kasir
client.post("/logout")

# 4. Login sebagai pemilik (pak_joko / joko12345)
client.post("/login", data={"username": "pak_joko", "password": "joko12345"})

# Pemilik membuka form tambah menu
res_pemilik_tambah = client.get("/menu/tambah")
assert res_pemilik_tambah.status_code == 200
assert "Tambah Menu Baru" in res_pemilik_tambah.get_data(as_text=True)
print("  [LULUS] Skenario 4: Pemilik membuka form tambah menu berhasil (200 OK).")

print(">>> SELURUH 4 UJI PERAN LANGKAH 5 LULUS 100% <<<")
