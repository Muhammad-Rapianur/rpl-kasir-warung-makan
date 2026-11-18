"""Seed data transaksi awal untuk Langkah 3 Jobsheet 10."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import models

with models.koneksi() as db:
    existing = db.execute(
        "SELECT COUNT(*) FROM transaksi WHERE nomor_transaksi LIKE"
        " 'TRX-20261119-%'"
    ).fetchone()[0]
    if existing == 0:
        # Transaksi 1: Dine-in
        db.execute(
            """
            INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, nomor_meja, metode_pembayaran, uang_diterima, pengguna_id)
            VALUES ('TRX-20261119-001', '2026-11-19 11:30:00', 'dine_in', '03', 'tunai', 50000, 2)
            """
        )
        t1_id = db.execute(
            "SELECT id FROM transaksi WHERE nomor_transaksi ="
            " 'TRX-20261119-001'"
        ).fetchone()["id"]
        # Ambil menu Ayam Goreng, Nasi Putih, Es Teh
        ayam = db.execute(
            "SELECT id, harga FROM menu WHERE nama = 'Ayam Goreng'"
        ).fetchone()
        nasi = db.execute(
            "SELECT id, harga FROM menu WHERE nama = 'Nasi Putih Pulen' OR nama"
            " = 'Nasi Putih'"
        ).fetchone()
        esteh = db.execute(
            "SELECT id, harga FROM menu WHERE nama = 'Es Teh Manis'"
        ).fetchone()

        db.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah,"
            " harga_satuan) VALUES (?, ?, 2, ?)",
            (t1_id, ayam["id"], ayam["harga"]),
        )
        db.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah,"
            " harga_satuan) VALUES (?, ?, 2, ?)",
            (t1_id, nasi["id"], nasi["harga"]),
        )
        db.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah,"
            " harga_satuan) VALUES (?, ?, 2, ?)",
            (t1_id, esteh["id"], esteh["harga"]),
        )

        # Transaksi 2: Take-away (QRIS)
        db.execute(
            """
            INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, nomor_meja, metode_pembayaran, uang_diterima, pengguna_id)
            VALUES ('TRX-20261119-002', '2026-11-19 12:15:00', 'take_away', NULL, 'qris', 22000, 2)
            """
        )
        t2_id = db.execute(
            "SELECT id FROM transaksi WHERE nomor_transaksi ="
            " 'TRX-20261119-002'"
        ).fetchone()["id"]
        bak = db.execute(
            "SELECT id, harga FROM menu WHERE nama = 'Ayam Bakar'"
        ).fetchone()

        db.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah,"
            " harga_satuan) VALUES (?, ?, 1, ?)",
            (t2_id, bak["id"], bak["harga"]),
        )
        db.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah,"
            " harga_satuan) VALUES (?, ?, 1, ?)",
            (t2_id, nasi["id"], nasi["harga"]),
        )
        print("2 Data transaksi awal berhasil dimasukkan.")
    else:
        print("Data transaksi sudah ada.")
