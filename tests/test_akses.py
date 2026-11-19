"""Matriks Hak Akses HTTP: rute x peran (tamu, kasir, pemilik).
Berkas: tests/test_akses.py
Sesuai Jobsheet 13 Langkah 9 dan Lampiran D.4.
"""
import pytest

# Matriks Rute: (metode, path, status_tamu, status_kasir, status_pemilik)
MATRIKS_AKSES = [
    # Katalog Menu: Tamu 302, Kasir 200 (Boleh lihat katalog), Pemilik 200
    ("GET", "/menu", 302, 200, 200),
    # Rute Terproteksi Pemilik Saja (Kasir harus 403, Tamu harus 302 Redirect)
    ("GET", "/menu/tambah", 302, 403, 200),
    ("GET", "/kategori", 302, 403, 200),
    ("GET", "/kategori/tambah", 302, 403, 200),
    # Rute Operasional Kasir & Pemilik (Semua Peran Login Boleh Akses)
    ("GET", "/transaksi", 302, 200, 200),
    ("GET", "/transaksi/tambah", 302, 200, 200),
]


@pytest.mark.parametrize("metode, alamat, utk_tamu, utk_kasir, utk_pemilik", MATRIKS_AKSES)
def test_matriks_akses_rute_peran(tamu, kasir, pemilik, metode, alamat, utk_tamu, utk_kasir, utk_pemilik):
    """Memverifikasi hak akses setiap rute terhadap peran pengguna (Tamu, Kasir, Pemilik)."""
    assert tamu.open(alamat, method=metode).status_code == utk_tamu, f"Tamu pada {alamat} harus {utk_tamu}"
    assert kasir.open(alamat, method=metode).status_code == utk_kasir, f"Kasir pada {alamat} harus {utk_kasir}"
    assert pemilik.open(alamat, method=metode).status_code == utk_pemilik, f"Pemilik pada {alamat} harus {utk_pemilik}"


def test_kasir_dilarang_hapus_menu_lewat_post(kasir, pemilik, kirim):
    """Kasir dilarang memicu penghapusan menu via HTTP POST (wajib mengembalikan 403 Forbidden)."""
    # 1. Pemilik membuat menu uji
    kirim(pemilik, "/menu/tambah", nama="Es Kelapa Muda", kategori_id="1", harga="8000", status="tersedia")

    # 2. Kasir mencoba menghapus menu id 1
    respon = kirim(kasir, "/menu/1/hapus", ikuti=False)
    assert respon.status_code == 403, "Aksi hapus oleh kasir harus ditolak dengan status HTTP 403"


def test_post_tanpa_token_csrf_ditolak_400(pemilik):
    """Permintaan HTTP POST tanpa menyertakan token CSRF sah wajib ditolak dengan HTTP 400 Bad Request."""
    respon = pemilik.post("/menu/tambah", data={"nama": "Kopi Hitam", "harga": "5000", "kategori_id": "1"})
    assert respon.status_code == 400, "Permintaan POST tanpa token CSRF wajib menghasilkan 400 Bad Request"
