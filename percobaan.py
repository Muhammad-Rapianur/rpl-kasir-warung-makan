"""Pembatasan percobaan login (Rate Limiting in-memory).
(Jobsheet 12 - Langkah 12 / Lampiran E.1)

Membatasi maksimal 5 kegagalan per 5 menit per kombinasi alamat IP dan nama pengguna.
Logika menerima argumen waktu (sekarang) agar dapat diuji secara otomatis dan terukur.
"""
import time

BATAS = 5        # Jumlah percobaan login gagal maksimum yang diizinkan
JENDELA = 300    # Durasi jendela waktu (300 detik = 5 menit)

_gagal = {}


def _bersihkan(kunci, sekarang):
    """Menghapus catatan percobaan gagal yang sudah melewati batas jendela waktu (5 menit)."""
    _gagal[kunci] = [t for t in _gagal.get(kunci, []) if sekarang - t < JENDELA]


def terkunci(kunci, sekarang=None):
    """Memeriksa apakah kombinasi kunci IP|username sedang dalam status terkunci."""
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    return len(_gagal.get(kunci, [])) >= BATAS


def catat_gagal(kunci, sekarang=None):
    """Mencatat satu kejadian kegagalan login untuk kunci IP|username."""
    sekarang = time.monotonic() if sekarang is None else sekarang
    _bersihkan(kunci, sekarang)
    if kunci not in _gagal:
        _gagal[kunci] = []
    _gagal[kunci].append(sekarang)


def reset(kunci):
    """Mereset catatan kegagalan setelah login berhasil."""
    _gagal.pop(kunci, None)
