"""Lapisan Logika Bisnis (Business Logic Layer) - KasirWarung.

Berisi validasi input, aturan bisnis kalkulasi, dan aturan data.
Dilarang memproses rendering HTML atau mengakses SQL secara langsung.
"""
import re
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash
import models

PERAN = ("pemilik", "kasir")

# Hash palsu berasam lambat untuk pertahanan serangan waktu (timing attack)
_HASH_PALSU = generate_password_hash("bukan-kata-sandi-sungguhan")


def _bilangan_positif(teks):
    """Ubah teks menjadi bilangan bulat positif (> 0), atau None bila tidak valid/negatif/kosong."""
    if teks is None:
        return None
    teks = str(teks).strip()
    if not teks.isdigit():
        return None
    nilai = int(teks)
    return nilai if nilai > 0 else None


def validasi_menu(form):
    """Validasi data form menu (nama, kategori_id, harga).

    Kembalikan tuple (data_bersih, daftar_galat).
    Aturan validasi mengikuti kamus data & SRS:
    - Nama hidangan tidak boleh kosong (minimal 2 karakter).
    - Kategori wajib dipilih.
    - Harga wajib berupa angka positif (> 0).
    """
    galat = []
    nama = (form.get("nama") or "").strip()
    kategori_id = form.get("kategori_id")
    harga_raw = form.get("harga")

    if not nama:
        galat.append("Nama menu hidangan wajib diisi.")
    elif len(nama) < 2:
        galat.append("Nama menu minimal terdiri dari 2 karakter.")

    try:
        kat_id = int(str(kategori_id).strip()) if kategori_id else None
        if not kat_id:
            galat.append("Kategori menu wajib dipilih.")
    except (ValueError, TypeError):
        kat_id = None
        galat.append("Kategori menu tidak valid.")

    harga = _bilangan_positif(harga_raw)
    if harga is None:
        galat.append(
            "Harga jual harus berupa bilangan bulat positif lebih besar dari 0 (contoh: 15000)."
        )

    data_bersih = {
        "nama": nama,
        "kategori_id": kat_id,
        "harga": harga,
    }
    return data_bersih, galat


def validasi_kategori(form):
    """Validasi form tambah/ubah kategori.

    - Nama kategori wajib diisi.
    - Minimal 3 karakter.
    """
    galat = []
    nama = (form.get("nama") or "").strip()

    if not nama:
        galat.append("Nama kategori wajib diisi.")
    elif len(nama) < 3:
        galat.append("Nama kategori minimal 3 karakter.")

    return {"nama": nama}, galat


def validasi_transaksi(form):
    """Validasi form pencatatan transaksi kasir baru (Langkah 4).

    Menguji menu_id, kuantitas, format tanggal, dan metode bayar.
    """
    galat = []

    # 1. Validasi Menu ID (Induk)
    menu_id_raw = form.get("menu_id")
    menu_id = None
    if not menu_id_raw or str(menu_id_raw).strip() == "":
        galat.append("Pilih menu hidangan.")
    else:
        try:
            menu_id = int(str(menu_id_raw).strip())
        except (ValueError, TypeError):
            galat.append("Pilihan menu tidak valid.")

    # 2. Validasi Jumlah (harus bilangan bulat > 0)
    jumlah_raw = form.get("jumlah")
    jumlah = None
    if not jumlah_raw or str(jumlah_raw).strip() == "":
        galat.append("Jumlah porsi harus berupa angka lebih dari 0.")
    else:
        teks_jml = str(jumlah_raw).strip()
        if not teks_jml.isdigit() or int(teks_jml) <= 0:
            galat.append("Jumlah porsi harus berupa angka lebih dari 0.")
        else:
            jumlah = int(teks_jml)

    # 3. Validasi Tanggal (Wajib format TTTT-BB-HH / ISO)
    tanggal_raw = (form.get("tanggal") or "").strip()
    if not tanggal_raw:
        galat.append("Tanggal transaksi wajib diisi.")
        tanggal_iso = date.today().isoformat()
    else:
        try:
            # Uji format TTTT-BB-HH (ISO)
            parsed_date = date.fromisoformat(tanggal_raw)
            # Simpan dengan jam saat ini
            waktu_sekarang = datetime.now().strftime("%H:%M:%S")
            tanggal_iso = f"{parsed_date.isoformat()} {waktu_sekarang}"
        except ValueError:
            galat.append("Tanggal harus berformat TTTT-BB-HH (contoh: 2026-11-19).")
            tanggal_iso = None

    # 4. Validasi Tipe Pesanan
    tipe_pesanan = form.get("tipe_pesanan", "dine_in")
    if tipe_pesanan not in ("dine_in", "take_away"):
        tipe_pesanan = "dine_in"

    nomor_meja = (form.get("nomor_meja") or "").strip() or None
    if tipe_pesanan == "dine_in" and not nomor_meja:
        nomor_meja = "01"  # Default nomor meja jika tidak diisi

    # 5. Validasi Metode Bayar & Uang Diterima
    metode_pembayaran = form.get("metode_pembayaran", "tunai")
    if metode_pembayaran not in ("tunai", "qris"):
        metode_pembayaran = "tunai"

    uang_raw = form.get("uang_diterima", "0")
    try:
        uang_diterima = int(str(uang_raw).strip()) if str(uang_raw).strip().isdigit() else 0
    except (ValueError, TypeError):
        uang_diterima = 0

    data = {
        "menu_id": menu_id,
        "jumlah": jumlah,
        "tanggal_waktu": tanggal_iso,
        "tipe_pesanan": tipe_pesanan,
        "nomor_meja": nomor_meja,
        "metode_pembayaran": metode_pembayaran,
        "uang_diterima": uang_diterima,
    }
    return data, galat


# ============================================================
# Modul Autentikasi & Akun Pengguna (Jobsheet 11 - Fitur H1/H2)
# ============================================================

def validasi_pengguna_baru(username, password, peran, nama_lengkap=""):
    """Validasi input registrasi akun baru.

    - username: 3-30 karakter alfanumerik atau garis bawah (_).
    - password: minimal 8 karakter.
    - peran: wajib 'pemilik' atau 'kasir'.
    - nama_lengkap: minimal 2 karakter.
    """
    galat = []
    usr = (username or "").strip()
    pwd = password or ""
    prn = (peran or "").strip()
    nama = (nama_lengkap or "").strip()

    if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", usr):
        galat.append("Nama pengguna harus terdiri dari 3–30 karakter alfanumerik atau garis bawah (_).")

    if len(pwd) < 8:
        galat.append("Kata sandi minimal terdiri dari 8 karakter.")

    if prn not in PERAN:
        galat.append("Peran pengguna harus 'pemilik' atau 'kasir'.")

    if not nama or len(nama) < 2:
        galat.append("Nama lengkap pengguna minimal 2 karakter.")

    return galat


def buat_pengguna(username, password, peran, nama_lengkap=""):
    """Mendaftarkan akun baru ke basis data dengan kata sandi ter-hash scrypt/pbkdf2."""
    galat = validasi_pengguna_baru(username, password, peran, nama_lengkap)
    if not galat:
        hash_pwd = generate_password_hash(password)
        models.tambah_pengguna(username, hash_pwd, nama_lengkap, peran)
    return galat


def autentikasi(username, password):
    """Verifikasi kredensial pengguna saat login (Jobsheet 11 - H2).

    Mengembalikan record pengguna jika username & password cocok, atau None jika gagal.
    Menggunakan _HASH_PALSU saat username tidak ada demi mencegah serangan waktu (timing attack).
    """
    usr = (username or "").strip()
    pwd = password or ""

    pengguna = models.cari_pengguna(usr)
    # Gunakan hash pengguna asli bila ada, atau hash palsu bila tidak ada
    hash_pembanding = pengguna["password_hash"] if pengguna else _HASH_PALSU

    cocok = check_password_hash(hash_pembanding, pwd)
    if pengguna and cocok:
        return pengguna
    return None



