"""Skrip Pembuat Akun Pengguna Awal (Jobsheet 11 - Langkah 3 / Lampiran B.3).

Kata sandi dibaca secara tersembunyi via modul getpass dari terminal.
Kata sandi mentah TIDAK PERNAH ditulis dalam kode dan TIDAK IKUT di-commit ke Git.
"""
import getpass
import sqlite3
import sys

import models
import services


def main():
    models.init_db()

    # Mendukung masukan non-interaktif via argumen CLI (misal untuk testing otomatis)
    if len(sys.argv) == 5:
        username = sys.argv[1].strip()
        peran = sys.argv[2].strip()
        nama_lengkap = sys.argv[3].strip()
        password = sys.argv[4]
    else:
        print("=== BUAT AKUN PENGGUNA BARU (KASIRWARUNG) ===")
        username = input("Nama pengguna (username) : ").strip()
        peran = input("Peran (pemilik / kasir)   : ").strip().lower()
        nama_lengkap = input("Nama lengkap              : ").strip()
        password = getpass.getpass("Kata sandi (min. 8 huruf) : ")

    try:
        galat = services.buat_pengguna(username, password, peran, nama_lengkap)
    except sqlite3.IntegrityError:
        galat = [f"Nama pengguna '{username}' sudah terdaftar di sistem."]

    if galat:
        print("\n[GAGAL DIBUAT]:")
        for g in galat:
            print(f" - {g}")
        sys.exit(1)
    else:
        print(f"\n[SUKSES] Akun '{username}' ({peran}) atas nama '{nama_lengkap}' berhasil dibuat!")


if __name__ == "__main__":
    main()
