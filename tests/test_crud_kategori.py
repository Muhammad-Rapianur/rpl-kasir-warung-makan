"""Test script untuk validasi Langkah 14 (CRUD Entitas Kedua: Kategori)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

print("=== 1. UJI DAFTAR KATEGORI (READ) ===")
res_list = client.get("/kategori")
assert res_list.status_code == 200
html_list = res_list.get_data(as_text=True)
assert "Daftar Kategori Hidangan" in html_list
assert "Makanan Utama" in html_list
assert "menu" in html_list
print("  [LULUS] Halaman daftar kategori menampilkan nama & jumlah menu.")

print("\n=== 2. UJI TAMBAH KATEGORI (CREATE) ===")
# 2a. Tambah valid
res_tambah = client.post(
    "/kategori/tambah",
    data={"nama": "Aneka Sambal Nusantara"},
    follow_redirects=True,
)
assert res_tambah.status_code == 200
html_tambah = res_tambah.get_data(as_text=True)
assert "Aneka Sambal Nusantara" in html_tambah
print("  [LULUS] Tambah kategori valid berhasil dan tampil di daftar.")

# 2b. Tambah kosong
res_kosong = client.post("/kategori/tambah", data={"nama": ""})
assert res_kosong.status_code == 200
assert (
    "Nama kategori wajib diisi" in res_kosong.get_data(as_text=True)
)
print("  [LULUS] Nama kategori kosong ditolak dengan pesan galat.")

# 2c. Tambah duplikat
res_dup = client.post(
    "/kategori/tambah", data={"nama": "Aneka Sambal Nusantara"}
)
assert res_dup.status_code == 200
assert "sudah terdaftar" in res_dup.get_data(as_text=True)
print("  [LULUS] Nama kategori duplikat ditolak.")

print("\n=== 3. UJI UBAH KATEGORI (UPDATE) ===")
# Ambil ID kategori yang baru dibuat
with models.koneksi() as db:
    kat = db.execute(
        "SELECT id FROM kategori WHERE nama = 'Aneka Sambal Nusantara'"
    ).fetchone()
kat_id = kat["id"]

# 3a. Ubah valid
res_ubah = client.post(
    f"/kategori/{kat_id}/ubah",
    data={"nama": "Sambal Spesial"},
    follow_redirects=True,
)
assert res_ubah.status_code == 200
assert "Sambal Spesial" in res_ubah.get_data(as_text=True)
print("  [LULUS] Ubah nama kategori berhasil.")

# 3b. 404 ID fiktif
res_404 = client.get("/kategori/999/ubah")
assert res_404.status_code == 404
print("  [LULUS] Kategori ID 999 menghasilkan 404.")

print("\n=== 4. UJI HAPUS KATEGORI (DELETE) ===")
# 4a. GET ditolak (405)
res_get_hapus = client.get(f"/kategori/{kat_id}/hapus")
assert res_get_hapus.status_code == 405
print("  [LULUS] Hapus via GET ditolak (405 Method Not Allowed).")

# 4b. Hapus kategori yang masih memiliki menu (Kategori 1 'Makanan Utama')
res_fk = client.post("/kategori/1/hapus", follow_redirects=True)
assert res_fk.status_code == 200
html_fk = res_fk.get_data(as_text=True)
assert "tidak dapat dihapus karena masih digunakan" in html_fk
assert models.ambil_kategori(1) is not None
print("  [LULUS] Kategori yang terikat menu ditolak dihapus (FK restrict).")

# 4c. Hapus kategori kosong (Sambal Spesial)
res_del = client.post(f"/kategori/{kat_id}/hapus", follow_redirects=True)
assert res_del.status_code == 200
assert models.ambil_kategori(kat_id) is None
print("  [LULUS] Kategori bebas berhasil dihapus dari database.")

print("\n>>> SELURUH UJI CRUD KATEGORI (LANGKAH 14) LULUS 100% <<<")
