"""Uji partisi ekuivalen dan nilai batas (BVA/EP) untuk aturan validasi kasir warung makan.
Berkas: tests/test_validasi.py
Sesuai Jobsheet 13 Langkah 5 & 6 dan Lampiran D.2.
"""
import pytest
import services


def menu_form(**ubah):
    """Helper pembuat data form menu kasir warung."""
    form = {
        "nama": "Ayam Bakar Madu",
        "kategori_id": "1",
        "harga": "25000",
        "status": "tersedia",
    }
    form.update(ubah)
    return form


# ============================================================================
# TC-01..TC-12: Harga Menu Makanan/Minuman (BVA & Partisi Ekuivalen)
# Batas: 1 s.d. 1.000.000.000 (1 Miliar Rupiah)
# ============================================================================
@pytest.mark.parametrize(
    "harga, valid",
    [
        ("1", True),  # TC-02: Batas bawah valid
        ("25000", True),  # TC-03: Nilai tipikal menu warung
        (" 15000 ", True),  # TC-04: Spasi luar dipangkas
        ("1000000000", True),  # TC-05: Batas atas valid (1 Miliar)
        ("0", False),  # TC-01: Batas bawah invalid (harga 0)
        ("-1", False),  # TC-06: Di bawah batas bawah (negatif)
        ("15000.50", False),  # TC-07: Pecahan desimal
        ("gratis", False),  # TC-08: Bukan angka
        ("", False),  # TC-09: String kosong
        ("1000000001", False),  # TC-10: Tepat di atas batas atas (1 Miliar + 1)
        ("9" * 30, False),  # TC-11: 30 digit angka raksasa (anti overflow)
        ("²", False),  # TC-12: Angka Unicode bukan 0-9 ASCII
    ],
)
def test_validasi_harga_menu(harga, valid):
    """Menguji penanganan harga menu makanan dengan asersi spesifik."""
    try:
        data, galat = services.validasi_menu(menu_form(harga=harga))
        sukses = (len(galat) == 0)
    except Exception:
        # Jika terjadi crash/unhandled exception (mis. ValueError '²' atau OverflowError), uji harus gagal
        sukses = False

    assert sukses is valid, f"Pengujian harga '{harga}' gagal. Diharapkan valid={valid}, aktual sukses={sukses}"
    if valid:
        assert data["harga"] == int(harga.strip())


# ============================================================================
# TC-13..TC-15: Nama Menu Hidangan
# ============================================================================
@pytest.mark.parametrize(
    "nama, valid",
    [
        ("Soto Ayam Lamongan", True),  # Nama valid
        ("   ", False),  # Hanya spasi
        ("", False),  # Kosong
        ("A", False),  # 1 karakter (kurang dari batas minimum 2)
    ],
)
def test_validasi_nama_menu(nama, valid):
    """Menguji validasi nama menu hidangan."""
    data, galat = services.validasi_menu(menu_form(nama=nama))
    assert (len(galat) == 0) is valid


# ============================================================================
# TC-16..TC-19: Jumlah Porsi Pesanan (BVA & Partisi Ekuivalen)
# Batas: Minimal 1 porsi
# ============================================================================
@pytest.mark.parametrize(
    "jumlah, valid",
    [
        ("1", True),  # TC-16: Batas bawah valid
        ("5", True),  # Nilai tipikal porsi
        ("0", False),  # TC-17: Batas bawah invalid (0 porsi)
        ("-1", False),  # TC-18: Porsi negatif
        ("dua", False),  # TC-19: Teks non-angka
        ("²", False),  # Unicode digit bukan ASCII
    ],
)
def test_validasi_jumlah_porsi_transaksi(jumlah, valid):
    """Menguji kuantitas porsi pesanan pada pencatatan transaksi kasir."""
    form = {
        "menu_id": "1",
        "jumlah": jumlah,
        "tanggal": "2026-11-20",
        "tipe_pesanan": "dine_in",
        "nomor_meja": "05",
        "metode_pembayaran": "tunai",
        "uang_diterima": "50000",
    }
    data, galat = services.validasi_transaksi(form)
    assert (len(galat) == 0) is valid


# ============================================================================
# Validasi Format Tanggal Transaksi Penjualan (TTTT-BB-HH)
# ============================================================================
@pytest.mark.parametrize(
    "tanggal, valid",
    [
        ("2026-11-20", True),  # Format ISO standar valid
        ("2026-02-30", False),  # Tanggal kalender tidak ada
        ("20-11-2026", False),  # Urutan terbalik (HH-BB-TTTT)
        ("20261120", False),  # Tanpa tanda hubung
        ("", False),  # Kosong
    ],
)
def test_validasi_tanggal_transaksi(tanggal, valid):
    """Menguji kepatuhan format tanggal transaksi sesuai standar ISO YYYY-MM-DD."""
    form = {
        "menu_id": "1",
        "jumlah": "1",
        "tanggal": tanggal,
        "tipe_pesanan": "take_away",
        "metode_pembayaran": "tunai",
        "uang_diterima": "25000",
    }
    data, galat = services.validasi_transaksi(form)
    assert (len(galat) == 0) is valid


# ============================================================================
# TC-27..TC-28: Registrasi Pengguna Kasir/Pemilik (BVA Username & Password)
# ============================================================================
@pytest.mark.parametrize(
    "username, password, valid",
    [
        ("siti_kasir", "siti12345", True),  # Nilai tipikal valid
        ("usr", "12345678", True),  # Batas bawah username 3 karakter & password 8 karakter
        ("us", "12345678", False),  # TC-27: Username 2 karakter (invalid)
        ("u" * 30, "12345678", True),  # Username 30 karakter (batas atas valid)
        ("u" * 31, "12345678", False),  # Username 31 karakter (invalid)
        ("kasir_budi", "1234567", False),  # TC-28: Password 7 karakter (invalid)
    ],
)
def test_validasi_pengguna_baru(username, password, valid):
    """Menguji batasan panjang username dan kekuatan password akun kasir."""
    galat = services.validasi_pengguna_baru(username, password, "kasir", "Kasir Uji")
    assert (len(galat) == 0) is valid
