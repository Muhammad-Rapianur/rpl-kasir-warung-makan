"""Uji regresi cepat: jalankan  python tests/uji_cepat.py  dari folder proyek.
Memakai basis data sementara, sehingga kasir_warung.db tidak tersentuh.
(Jobsheet 11 - Langkah 12: Pengujian Lengkap Autentikasi, Otorisasi, CRUD, dan Transaksi)
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
import services

c = aplikasi.app.test_client()


def kirim(url, **data):
    return c.post(url, data=data, follow_redirects=True)


def ada(teks, hasil):
    assert teks in hasil.get_data(as_text=True), f"Tidak ditemukan: {teks!r}"


print("=== MEMULAI SUITE UJI REGRESI CEPAT JOBSHEET 11 (BASIS DATA SEMENTARA) ===")

# --- 1. MODUL AUTENTIKASI & KEAMANAN AKUN (JOBSHEET 11) ---
# Buat akun pengujian di basis data sementara
services.buat_pengguna("pemilik_uji", "password123", "pemilik", "Pemilik Toko")
services.buat_pengguna("kasir_uji", "password123", "kasir", "Kasir Toko")

# Buktikan password tersimpan sebagai hash
pengguna_db = models.cari_pengguna("pemilik_uji")
assert pengguna_db["password_hash"].startswith("scrypt:") or pengguna_db["password_hash"].startswith("pbkdf2:")
assert "password123" not in pengguna_db["password_hash"]

# Akses anonim ditolak dan dialihkan ke login
res_anonim = c.get("/menu", follow_redirects=False)
assert res_anonim.status_code == 302
assert "/login" in res_anonim.headers["Location"]
assert "next=/menu" in res_anonim.headers["Location"]

# Kredensial salah (password salah vs username fiktif) memberikan pesan galat identik
res_salah1 = c.post("/login", data={"username": "pemilik_uji", "password": "salahpassword"})
res_salah2 = c.post("/login", data={"username": "user_palsu", "password": "sembarangpassword"})
ada("Nama pengguna atau kata sandi salah.", res_salah1)
ada("Nama pengguna atau kata sandi salah.", res_salah2)

# Open redirect luar situs ditolak
res_open = c.post("/login?next=https://situs-jahat.example", data={"username": "pemilik_uji", "password": "password123"}, follow_redirects=False)
assert res_open.status_code == 302
assert "situs-jahat.example" not in res_open.headers["Location"]

# Logout dari sesi pemilik sebelumnya
c.post("/logout")
print("  [OK] Modul Autentikasi: Hash, pesan seragam, dan anti open-redirect teruji.")

# --- 2. MODUL OTORISASI PERAN (KASIR VS PEMILIK) ---
# Login sebagai kasir
res_login_kasir = c.post("/login", data={"username": "kasir_uji", "password": "password123"}, follow_redirects=True)
assert res_login_kasir.status_code == 200

# Kasir membuka katalog (diizinkan)
res_kasir_menu = c.get("/menu")
assert res_kasir_menu.status_code == 200
assert "+ Tambah Menu Baru" not in res_kasir_menu.get_data(as_text=True)

# Kasir mencoba membuka form tambah menu (ditolak 403)
assert c.get("/menu/tambah").status_code == 403
# Kasir mencoba POST hapus menu (ditolak 403)
assert c.post("/menu/1/hapus").status_code == 403
# Kasir mencoba buka kategori (ditolak 403)
assert c.get("/kategori").status_code == 403

# Kasir keluar
c.post("/logout")

# Login sebagai pemilik
c.post("/login", data={"username": "pemilik_uji", "password": "password123"}, follow_redirects=True)
res_pemilik_menu = c.get("/menu")
assert res_pemilik_menu.status_code == 200
assert "+ Tambah Menu Baru" in res_pemilik_menu.get_data(as_text=True)
print("  [OK] Modul Otorisasi Peran: Kasir 403 pada rute terlarang & Pemilik lolos teruji.")

# --- 3. MODUL MENU (CRUD OLEH PEMILIK) ---
ada("Daftar Menu Warung Makan", c.get("/menu"))

# Tambah menu
res_t1 = kirim("/menu/tambah", nama="Nasi Pecel Khas Sampit", kategori_id=1, harga=12000)
ada("berhasil ditambahkan", res_t1)

# Tolak nama duplikat
res_dup = kirim("/menu/tambah", nama="Nasi Pecel Khas Sampit", kategori_id=1, harga=15000)
ada("sudah terdaftar", res_dup)

# Ambil ID menu yang baru dibuat
id_pecel = [m['id'] for m in models.cari_menu("Nasi Pecel Khas Sampit")][0]

# Ubah menu
res_u1 = kirim(f"/menu/{id_pecel}/ubah", nama="Nasi Pecel Komplit", kategori_id=1, harga=14000, status="tersedia")
ada("berhasil diperbarui", res_u1)
assert models.ambil_menu(id_pecel)["harga"] == 14000
print("  [OK] Modul Menu CRUD dasar (oleh pemilik) berfungsi.")

# --- 4. MODUL PENCARIAN DAN PENYARINGAN ---
hasil_cari = c.get("/menu?q=Pecel")
ada("Nasi Pecel Komplit", hasil_cari)

# Karakter % dinetralkan (wildcard escape)
hasil_wildcard = c.get("/menu?q=%25")
ada("Tidak ada menu hidangan yang cocok", hasil_wildcard)

# Injeksi SQL dinetralkan
hasil_sql = c.get("/menu?q=' OR 1=1 --")
ada("Tidak ada menu hidangan yang cocok", hasil_sql)
print("  [OK] Pencarian aman (LIKE ? ESCAPE '\\') & filter berfungsi.")

# --- 5. MODUL TRANSAKSI RELASIONAL (Dua Tabel) ---
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

# Validasi masukan transaksi
ada("Jumlah porsi harus berupa angka lebih dari 0", kirim("/transaksi/tambah", menu_id=id_pecel, jumlah=-2, tanggal="2026-11-19"))
ada("Pilih menu hidangan", kirim("/transaksi/tambah", menu_id="", jumlah=1, tanggal="2026-11-19"))
ada("Tanggal harus berformat TTTT-BB-HH", kirim("/transaksi/tambah", menu_id=id_pecel, jumlah=1, tanggal="19-11-2026"))
print("  [OK] Transaksi dua tabel & validasi masukan berfungsi.")

# --- 6. PROTEKSI FOREIGN KEY & ATOMISITAS ---
# Menu id_pecel terikat transaksi -> tolak hapus
res_hapus = kirim(f"/menu/{id_pecel}/hapus")
ada("tidak dapat dihapus", res_hapus)
assert c.get(f"/menu/{id_pecel}/hapus").status_code == 405  # Wajib tolak GET

# Uji atomisitas rollback
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
print("  [OK] Proteksi Foreign Key RESTRICT & atomisitas rollback terbukti 100%.")

print("\n=========================================================")
print(">>> SEMUA UJI REGRESI JOBSHEET 11 LULUS 100% (SUKSES) <<<")
print("=========================================================")
