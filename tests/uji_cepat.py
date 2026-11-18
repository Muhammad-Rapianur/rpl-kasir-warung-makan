"""Uji regresi cepat: jalankan  python tests/uji_cepat.py  dari folder proyek.
Memakai basis data sementara, sehingga kasir_warung.db tidak tersentuh.
(Jobsheet 12 - Langkah 14 / Lampiran E.3: Pengujian Lengkap CSRF, Rate Limit, Header, & RBAC)
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
import percobaan
import services

c = aplikasi.app.test_client()


def _siapkan_token(client, token="token-keamanan-uji"):
    """Menyisipkan token CSRF ke dalam sesi client testing."""
    with client.session_transaction() as sess:
        sess.setdefault("csrf_token", token)
        return sess["csrf_token"]


def kirim(url, ikuti=True, **data):
    """Helper pengiriman POST otomatis dengan menyertakan token CSRF yang sah."""
    token = _siapkan_token(c)
    data.setdefault("csrf_token", token)
    return c.post(url, data=data, follow_redirects=ikuti)


def ada(teks, hasil):
    assert teks in hasil.get_data(as_text=True), f"Tidak ditemukan: {teks!r}"


print("=== MEMULAI SUITE UJI REGRESI CEPAT JOBSHEET 12 (LENGKAP) ===")

# --- 1. UJI PROTEKSI CSRF (LANGKAH 11) ---
# POST tanpa token CSRF wajib ditolak dengan HTTP 400 Bad Request
res_tanpa_csrf = c.post("/login", data={"username": "kasir", "password": "any"})
assert res_tanpa_csrf.status_code == 400
ada("CSRF Gagal", res_tanpa_csrf)

# POST dengan token salah wajib ditolak 400
res_csrf_salah = c.post("/login", data={"username": "kasir", "password": "any", "csrf_token": "token_palsu"})
assert res_csrf_salah.status_code == 400
print("  [OK] Proteksi CSRF: Permintaan POST tanpa token sah ditolak 400 Bad Request.")

# --- 2. UJI HEADER KEAMANAN RESPONS (LANGKAH 13) ---
headers = c.get("/login").headers
assert headers.get("X-Content-Type-Options") == "nosniff"
assert headers.get("X-Frame-Options") == "DENY"
assert headers.get("Referrer-Policy") == "same-origin"
print("  [OK] Header Keamanan: nosniff, DENY, dan same-origin terpasang aktif.")

# --- 3. UJI RATE LIMITING & PEMBATASAN LOGIN BRUTE-FORCE (LANGKAH 12) ---
kunci_korban = "127.0.0.1|korban_bruteforce"
percobaan.reset(kunci_korban)

# Lakukan 5 kali percobaan gagal
for _ in range(percobaan.BATAS):
    r_gagal = kirim("/login", ikuti=False, username="korban_bruteforce", password="password_salah")
    assert r_gagal.status_code == 401

# Percobaan ke-6 wajib ditolak dengan HTTP 429 Too Many Requests
r_kunci = kirim("/login", ikuti=False, username="korban_bruteforce", password="password_benar")
assert r_kunci.status_code == 429
ada("Terlalu banyak percobaan", r_kunci)
print("  [OK] Rate Limiter: Percobaan ke-6 diblokir dengan HTTP 429 Too Many Requests.")

# --- 4. MODUL AUTENTIKASI & KEAMANAN AKUN (JOBSHEET 11) ---
services.buat_pengguna("pemilik_uji", "password123", "pemilik", "Pemilik Toko")
services.buat_pengguna("kasir_uji", "password123", "kasir", "Kasir Toko")

# Password tersimpan sebagai hash
pengguna_db = models.cari_pengguna("pemilik_uji")
assert pengguna_db["password_hash"].startswith("scrypt:") or pengguna_db["password_hash"].startswith("pbkdf2:")

# Tamu dialihkan ke login
res_anonim = c.get("/menu", follow_redirects=False)
assert res_anonim.status_code == 302
assert "/login" in res_anonim.headers["Location"]

# Open redirect luar situs ditolak
res_open = kirim("/login?next=https://situs-jahat.example", ikuti=False, username="pemilik_uji", password="password123")
assert res_open.status_code == 302
assert "situs-jahat.example" not in res_open.headers["Location"]

# Logout
kirim("/logout")
print("  [OK] Autentikasi: Hash scrypt, anti open-redirect, dan sesi teruji.")

# --- 5. MODUL OTORISASI PERAN (KASIR VS PEMILIK) ---
# Login sebagai kasir
kirim("/login", username="kasir_uji", password="password123")

# Kasir membuka katalog (200 OK tanpa tombol tambah)
res_kasir_menu = c.get("/menu")
assert res_kasir_menu.status_code == 200
assert "+ Tambah Menu Baru" not in res_kasir_menu.get_data(as_text=True)

# Aksi terlarang kasir ditolak 403 Forbidden
assert c.get("/menu/tambah").status_code == 403
assert kirim("/menu/1/hapus", ikuti=False).status_code == 403
assert c.get("/kategori").status_code == 403

# Kasir keluar
kirim("/logout")

# Login sebagai pemilik
kirim("/login", username="pemilik_uji", password="password123")
res_pemilik_menu = c.get("/menu")
assert res_pemilik_menu.status_code == 200
assert "+ Tambah Menu Baru" in res_pemilik_menu.get_data(as_text=True)
print("  [OK] Otorisasi Peran: Kasir 403 pada rute terlarang & Pemilik lolos penuh.")

# --- 6. MODUL MENU (CRUD OLEH PEMILIK) ---
# Tambah menu
res_t1 = kirim("/menu/tambah", nama="Nasi Pecel Khas Sampit", kategori_id=1, harga=12000)
ada("berhasil ditambahkan", res_t1)

id_pecel = [m['id'] for m in models.cari_menu("Nasi Pecel Khas Sampit")][0]

# Ubah menu
res_u1 = kirim(f"/menu/{id_pecel}/ubah", nama="Nasi Pecel Komplit", kategori_id=1, harga=14000, status="tersedia")
ada("berhasil diperbarui", res_u1)
assert models.ambil_menu(id_pecel)["harga"] == 14000
print("  [OK] Modul Menu CRUD: Berfungsi normal dengan CSRF token.")

# --- 7. MODUL PENCARIAN DAN PENYARINGAN ---
hasil_cari = c.get("/menu?q=Pecel")
ada("Nasi Pecel Komplit", hasil_cari)
hasil_wildcard = c.get("/menu?q=%25")
ada("Tidak ada menu hidangan yang cocok", hasil_wildcard)
print("  [OK] Pencarian aman (LIKE ? ESCAPE '\\') & filter berfungsi.")

# --- 8. MODUL TRANSAKSI RELASIONAL (Dua Tabel) ---
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
print("  [OK] Transaksi dua tabel & validasi masukan berfungsi.")

# --- 9. PROTEKSI FOREIGN KEY & ATOMISITAS ---
res_hapus = kirim(f"/menu/{id_pecel}/hapus")
ada("tidak dapat dihapus", res_hapus)

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
print(">>> SEMUA UJI REGRESI JOBSHEET 12 LULUS 100% (SUKSES) <<<")
print("=========================================================")
