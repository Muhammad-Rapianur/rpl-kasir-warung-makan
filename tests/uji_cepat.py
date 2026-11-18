"""Uji regresi cepat: jalankan  python tests/uji_cepat.py  dari folder proyek.
Memakai basis data sementara, sehingga kasir_warung.db tidak tersentuh.
(Jobsheet 10 - Langkah 12 / Lampiran C.3)
"""
import sys
import tempfile
from pathlib import Path

# Pasang root direktori proyek
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import models

# 1. Alihkan DB_PATH ke basis data sementara
temp_dir = tempfile.mkdtemp()
models.DB_PATH = Path(temp_dir) / "uji_kasir.db"
models.init_db()

import app as aplikasi

c = aplikasi.app.test_client()


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.get_data(as_text=True), f"Tidak ditemukan: {teks!r}"


print("=== MEMULAI SUITE UJI REGRESI CEPAT (ISOLASI SEMENTARA) ===")

# --- 1. MODUL MENU (CRUD DASAR) ---
ada("Daftar Menu Warung Makan", c.get("/menu"))

# Tambah menu
res_t1 = kirim("/menu/tambah", nama="Nasi Pecel Khas Sampit", kategori_id=1, harga=12000)
ada("berhasil ditambahkan", res_t1)

res_t2 = kirim("/menu/tambah", nama="Es Jeruk Segar Asli", kategori_id=2, harga=5000)
ada("berhasil ditambahkan", res_t2)

# Tolak nama duplikat
res_dup = kirim("/menu/tambah", nama="Nasi Pecel Khas Sampit", kategori_id=1, harga=15000)
ada("sudah terdaftar", res_dup)

# Ubah menu (gunakan menu yang baru saja ditambahkan)
id_pecel = [m['id'] for m in models.cari_menu("Nasi Pecel Khas Sampit")][0]
res_u1 = kirim(
    f"/menu/{id_pecel}/ubah",
    nama="Nasi Pecel Komplit",
    kategori_id=1,
    harga=14000,
    status="tersedia",
)
ada("berhasil diperbarui", res_u1)
assert models.ambil_menu(id_pecel)["harga"] == 14000
print("  [OK] Modul Menu CRUD dasar berfungsi.")

# --- 2. MODUL PENCARIAN DAN PENYARINGAN ---
hasil_cari = c.get("/menu?q=Pecel")
ada("Nasi Pecel Komplit", hasil_cari)
assert "Es Jeruk Segar Asli" not in hasil_cari.get_data(as_text=True)

# Karakter % dinetralkan
hasil_wildcard = c.get("/menu?q=%25")
ada("Tidak ada menu hidangan yang cocok", hasil_wildcard)

# Injeksi SQL gagal
hasil_sql = c.get("/menu?q=' OR 1=1 --")
ada("Tidak ada menu hidangan yang cocok", hasil_sql)
print("  [OK] Pencarian aman (LIKE ? ESCAPE '\\') & filter berfungsi.")

# --- 3. MODUL TRANSAKSI RELASIONAL (Dua Tabel) ---
ada("Riwayat Transaksi Penjualan", c.get("/transaksi"))

# Tambah transaksi valid (Dine-in)
res_trx = kirim(
    "/transaksi/tambah",
    menu_id=id_pecel,
    jumlah=2,
    tanggal="2026-11-19",
    tipe_pesanan="dine_in",
    nomor_meja="02",
    metode_pembayaran="tunai",
    uang_diterima=50000,
)
ada("berhasil dicatat", res_trx)
ada("Nasi Pecel Komplit (2x)", res_trx)

# Masukan tidak valid ditolak
ada(
    "Jumlah porsi harus berupa angka lebih dari 0",
    kirim("/transaksi/tambah", menu_id=id_pecel, jumlah=-2, tanggal="2026-11-19"),
)
ada(
    "Pilih menu hidangan",
    kirim("/transaksi/tambah", menu_id="", jumlah=1, tanggal="2026-11-19"),
)
ada(
    "Tanggal harus berformat TTTT-BB-HH",
    kirim("/transaksi/tambah", menu_id=id_pecel, jumlah=1, tanggal="19-11-2026"),
)
ada(
    "Menu hidangan tidak ditemukan",
    kirim("/transaksi/tambah", menu_id=999, jumlah=1, tanggal="2026-11-19"),
)
print("  [OK] Validasi transaksi induk-anak berfungsi.")

# --- 4. PROTEKSI KUNCI ASING ---
# Menu id_pecel sudah ada di detail_transaksi -> tolak hapus
res_hapus = kirim(f"/menu/{id_pecel}/hapus")
ada("tidak dapat dihapus", res_hapus)
assert c.get(f"/menu/{id_pecel}/hapus").status_code == 405  # Wajib tolak GET
print("  [OK] Proteksi foreign key RESTRICT dan HTTP POST aktif.")

# --- 5. UJI ATOMISITAS TRANSAKSI ---
total_awal = len(models.semua_transaksi())
import sqlite3

try:
    models.tambah_transaksi_dengan_detail(
        menu_id=999,
        jumlah=1,
        tanggal_waktu="2026-11-19 10:00:00",
        tipe_pesanan="take_away",
        nomor_meja=None,
        metode_pembayaran="tunai",
        uang_diterima=10000,
    )
except sqlite3.IntegrityError:
    pass

assert len(models.semua_transaksi()) == total_awal
print("  [OK] Uji atomisitas rollback multi-tabel terbukti 100%.")

print("\n=========================================")
print(">>> SEMUA UJI REGRESI LULUS (100%) <<<")
print("=========================================")
