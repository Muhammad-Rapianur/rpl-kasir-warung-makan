"""Test script untuk validasi Langkah 9 (Hapus Menu)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

# 1. Test GET /menu/1/hapus ditolak (405 Method Not Allowed)
res_get = client.get("/menu/1/hapus")
assert res_get.status_code == 405
print("  [LULUS] Uji 1: Membuka alamat hapus via GET menghasilkan 405 (tidak menghapus).")

# 2. Test hapus menu yang tidak terikat transaksi (buat menu baru untuk diuji hapus)
with models.koneksi() as db:
    db.execute(
        "INSERT INTO menu (nama, kategori_id, harga, status) VALUES ('Menu Uji Hapus', 1, 10000, 'tersedia')"
    )
    temp_menu = db.execute("SELECT id FROM menu WHERE nama = 'Menu Uji Hapus'").fetchone()

temp_id = temp_menu["id"]

res_hapus = client.post(f"/menu/{temp_id}/hapus", follow_redirects=True)
assert res_hapus.status_code == 200
html_hapus = res_hapus.get_data(as_text=True)
assert "berhasil dihapus" in html_hapus

# Pastikan sudah benar-benar hilang dari database
assert models.ambil_menu(temp_id) is None
print("  [LULUS] Uji 2: Data yang tidak terpakai berhasil dihapus dari database.")

# 3. Test hapus menu yang dirujuk tabel detail_transaksi (IntegrityError)
# Buat transaksi dummy yang memakai menu ID 1
with models.koneksi() as db:
    db.execute(
        """
        INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, metode_pembayaran, uang_diterima, pengguna_id)
        VALUES ('TRX-TEST-001', '2026-11-18 12:00:00', 'dine_in', 'tunai', 10000, 2)
        """
    )
    trx_id = db.execute(
        "SELECT id FROM transaksi WHERE nomor_transaksi = 'TRX-TEST-001'"
    ).fetchone()["id"]
    db.execute(
        """
        INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, harga_satuan)
        VALUES (?, 1, 2, 5000)
        """,
        (trx_id,),
    )

# Coba hapus menu ID 1 (yang baru saja dimasukkan ke detail_transaksi)
res_fk = client.post("/menu/1/hapus", follow_redirects=True)
assert res_fk.status_code == 200
html_fk = res_fk.get_data(as_text=True)
assert "tidak dapat dihapus karena sudah memiliki riwayat transaksi" in html_fk

# Pastikan menu ID 1 TETAP ADA di database
assert models.ambil_menu(1) is not None
print(
    "  [LULUS] Uji 3: Menu yang dipakai transaksi tidak terhapus & muncul pesan"
    " ramah."
)

# 4. Test hapus ID yang tidak ada (404)
res_404 = client.post("/menu/999/hapus")
assert res_404.status_code == 404
print("  [LULUS] Uji 4: Hapus menu ID 999 menghasilkan 404 Not Found.")

print("\n>>> SELURUH UJI LANGKAH 9 LULUS 100% <<<")
