"""Test script untuk validasi Langkah 4 & 5 Jobsheet 10.

(Form Pilihan Induk & Transaksi Atomik Dua Tabel)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

print("=== 1. UJI MASUKAN FORM LANGKAH 4 (6 SKENARIO) ===")

# Uji 1: Semua kolom valid
res1 = client.post(
    "/transaksi/tambah",
    data={
        "menu_id": "3",  # Ayam Goreng
        "jumlah": "2",
        "tanggal": "2026-11-19",
        "tipe_pesanan": "dine_in",
        "nomor_meja": "08",
        "metode_pembayaran": "tunai",
        "uang_diterima": "50000",
    },
    follow_redirects=True,
)
assert res1.status_code == 200
html1 = res1.get_data(as_text=True)
assert "berhasil dicatat" in html1
assert "Ayam Goreng (2x)" in html1
print("  [LULUS] Uji 1: Transaksi valid tersimpan & tampil di riwayat.")

# Uji 2: Induk menu belum dipilih
res2 = client.post(
    "/transaksi/tambah",
    data={"menu_id": "", "jumlah": "2", "tanggal": "2026-11-19"},
)
assert res2.status_code == 200
assert "Pilih menu hidangan" in res2.get_data(as_text=True)
print("  [LULUS] Uji 2: Induk belum dipilih ditolak dengan pesan jelas.")

# Uji 3: Jumlah 0 atau -3
res3 = client.post(
    "/transaksi/tambah",
    data={"menu_id": "3", "jumlah": "-3", "tanggal": "2026-11-19"},
)
assert res3.status_code == 200
assert (
    "Jumlah porsi harus berupa angka lebih dari 0" in res3.get_data(as_text=True)
)
print("  [LULUS] Uji 3: Jumlah negatif (-3) ditolak dengan pesan galat.")

# Uji 4: Jumlah teks non-angka 'abc'
res4 = client.post(
    "/transaksi/tambah",
    data={"menu_id": "3", "jumlah": "abc", "tanggal": "2026-11-19"},
)
assert res4.status_code == 200
assert (
    "Jumlah porsi harus berupa angka lebih dari 0" in res4.get_data(as_text=True)
)
print("  [LULUS] Uji 4: Jumlah teks 'abc' ditolak dengan pesan galat.")

# Uji 5: Tanggal non-ISO '10-11-2026'
res5 = client.post(
    "/transaksi/tambah",
    data={"menu_id": "3", "jumlah": "1", "tanggal": "10-11-2026"},
)
assert res5.status_code == 200
assert (
    "Tanggal harus berformat TTTT-BB-HH" in res5.get_data(as_text=True)
)
print("  [LULUS] Uji 5: Tanggal non-ISO ditolak dengan pesan format tanggal.")

# Uji 6: ID Induk menu 999 (fiktif)
res6 = client.post(
    "/transaksi/tambah",
    data={"menu_id": "999", "jumlah": "1", "tanggal": "2026-11-19"},
)
assert res6.status_code == 200
assert (
    "Menu hidangan tidak ditemukan" in res6.get_data(as_text=True)
)
print(
    "  [LULUS] Uji 6: ID induk fiktif 999 ditolak dengan pesan ramah (bukan"
    " 500)."
)

print(
    "\n=== 2. UJI TRANSAKSI ATOMIK DUA TABEL (LANGKAH 5 — with koneksi()) ==="
)
with models.koneksi() as db:
    total_trx_awal = db.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0]
    total_dtl_awal = db.execute(
        "SELECT COUNT(*) FROM detail_transaksi"
    ).fetchone()[0]

# Panggil fungsi penambahan transaksi dengan menu ID 999 yang tidak ada
import sqlite3

try:
    models.tambah_transaksi_dengan_detail(
        menu_id=999,
        jumlah=1,
        tanggal_waktu="2026-11-19 12:00:00",
        tipe_pesanan="take_away",
        nomor_meja=None,
        metode_pembayaran="tunai",
        uang_diterima=10000,
    )
    assert False, "Fungsi seharusnya melempar IntegrityError!"
except sqlite3.IntegrityError:
    print("  [LULUS] Exception IntegrityError tertangkap dengan benar.")

# Buktikan atomisitas: transaksi header TIDAK tertinggal di basis data
with models.koneksi() as db:
    total_trx_akhir = db.execute("SELECT COUNT(*) FROM transaksi").fetchone()[0]
    total_dtl_akhir = db.execute(
        "SELECT COUNT(*) FROM detail_transaksi"
    ).fetchone()[0]

assert (
    total_trx_akhir == total_trx_awal
), "FATAL: Terjadi kebocoran baris transaksi header (non-atomic rollback)!"
assert (
    total_dtl_akhir == total_dtl_awal
), "FATAL: Terjadi kebocoran baris detail_transaksi!"
print(
    f"  [LULUS] Atomisitas terbukti 100%! Data tetap konsisten: transaksi tetap"
    f" {total_trx_akhir}, detail tetap {total_dtl_akhir} (0 jejak sebagian)."
)

print("\n>>> SELURUH UJI LANGKAH 4 & 5 LULUS 100% <<<")
