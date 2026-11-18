"""Uji Langkah 6: Proteksi Foreign Key saat menghapus entitas induk (menu)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

print("=== UJI LANGKAH 6: PROTEKSI KUNCI ASING & HAPUS INDUK ===")

# Menu ID 3 (Ayam Goreng) sudah dipakai di detail_transaksi
res_terikat = client.post("/menu/3/hapus", follow_redirects=True)
assert res_terikat.status_code == 200
html_terikat = res_terikat.get_data(as_text=True)
assert "tidak dapat dihapus" in html_terikat or "riwayat" in html_terikat
print("  [LULUS] Hapus menu terikat transaksi berhasil ditolak dengan notifikasi ramah.")

# Buat menu baru sementara yang belum dipakai transaksi
with models.koneksi() as db:
    cursor = db.execute(
        "INSERT INTO menu (nama, kategori_id, harga, status) VALUES ('Menu Coba Hapus', 1, 10000, 'tersedia')"
    )
    id_baru = cursor.lastrowid

# Hapus menu baru yang bebas relasi
res_bebas = client.post(f"/menu/{id_baru}/hapus", follow_redirects=True)
assert res_bebas.status_code == 200
html_bebas = res_bebas.get_data(as_text=True)
assert "berhasil dihapus" in html_bebas
print("  [LULUS] Menu bebas transaksi berhasil dihapus dengan aman.")

print(">>> UJI LANGKAH 6 LULUS 100% <<<")
