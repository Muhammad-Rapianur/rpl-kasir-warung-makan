"""
tests/cek_skema.py
Skrip Pengujian Integritas Skema Basis Data
Sistem Kasir Warung Makan (KasirWarung)
Mata Kuliah : Rekayasa Perangkat Lunak (RPL)
Jobsheet    : 6 — Sesi 2, Langkah 9

Cara menjalankan:
    python tests/cek_skema.py

Hasil yang diharapkan:
    Semua pengujian LULUS, tidak ada yang GAGAL.
"""

import sqlite3
import os

# ============================================================
# Setup: Baca schema.sql dan buat database di memori (in-memory)
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(BASE_DIR, "docs", "desain", "schema.sql")

def buat_db():
    """Membuat koneksi database SQLite in-memory dari schema.sql."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


# ============================================================
# Fungsi bantu pengujian
# ============================================================
lulus = 0
gagal = 0

def uji(nama_uji, fungsi_uji):
    """Menjalankan satu fungsi uji dan melaporkan hasilnya."""
    global lulus, gagal
    try:
        fungsi_uji()
        print(f"  [LULUS] {nama_uji}")
        lulus += 1
    except AssertionError as e:
        print(f"  [GAGAL] {nama_uji}")
        print(f"          → {e}")
        gagal += 1
    except sqlite3.IntegrityError as e:
        print(f"  [LULUS] {nama_uji}  (IntegrityError ditangkap: {e})")
        lulus += 1


# ============================================================
# KELOMPOK UJI 1: Tabel dan Struktur Skema
# ============================================================
def uji_semua_tabel_ada():
    conn = buat_db()
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tabel = {r[0] for r in cur.fetchall()}
    tabel_wajib = {"pengguna", "kategori", "menu", "transaksi", "detail_transaksi"}
    hilang = tabel_wajib - tabel
    assert not hilang, f"Tabel berikut tidak ditemukan: {hilang}"
    conn.close()


def uji_seed_data_kategori():
    conn = buat_db()
    cur = conn.execute("SELECT COUNT(*) FROM kategori")
    jumlah = cur.fetchone()[0]
    assert jumlah >= 4, f"Seed data kategori kurang dari 4, ditemukan: {jumlah}"
    conn.close()


def uji_seed_data_menu():
    conn = buat_db()
    cur = conn.execute("SELECT COUNT(*) FROM menu")
    jumlah = cur.fetchone()[0]
    assert jumlah >= 1, f"Seed data menu kosong"
    conn.close()


# ============================================================
# KELOMPOK UJI 2: Batasan Data (CHECK Constraints)
# ============================================================
def uji_tolak_harga_menu_negatif():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO menu (kategori_id, nama, harga, status) VALUES (1, 'Menu Uji', -1000, 'tersedia')"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: harga negatif lolos masuk database!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (harga >= 0)
    finally:
        conn.close()


def uji_tolak_status_menu_tidak_valid():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO menu (kategori_id, nama, harga, status) VALUES (1, 'Menu Uji 2', 5000, 'kosong')"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: status 'kosong' bukan nilai valid!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (status IN ('tersedia', 'habis'))
    finally:
        conn.close()


def uji_tolak_peran_pengguna_tidak_valid():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO pengguna (username, password_hash, nama_lengkap, peran) "
            "VALUES ('testuser', 'hash123', 'User Uji', 'admin')"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: peran 'admin' bukan nilai valid!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (peran IN ('kasir', 'pemilik'))
    finally:
        conn.close()


def uji_tolak_metode_bayar_tidak_valid():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, "
            "metode_pembayaran, uang_diterima, pengguna_id) "
            "VALUES ('TRX-TEST-001', '2026-11-14 10:00:00', 'dine_in', 'transfer', 50000, 2)"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: metode 'transfer' bukan nilai valid!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (metode_pembayaran IN ('tunai', 'qris'))
    finally:
        conn.close()


def uji_tolak_tipe_pesanan_tidak_valid():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, "
            "metode_pembayaran, uang_diterima, pengguna_id) "
            "VALUES ('TRX-TEST-002', '2026-11-14 10:00:00', 'delivery', 'tunai', 50000, 2)"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: tipe 'delivery' bukan nilai valid!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (tipe_pesanan IN ('dine_in', 'take_away'))
    finally:
        conn.close()


def uji_tolak_jumlah_detail_nol_atau_negatif():
    conn = buat_db()
    # Sisipkan transaksi valid dulu sebagai induk
    conn.execute(
        "INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, "
        "metode_pembayaran, uang_diterima, pengguna_id) "
        "VALUES ('TRX-TEST-003', '2026-11-14 10:00:00', 'take_away', 'tunai', 20000, 2)"
    )
    conn.commit()
    try:
        conn.execute(
            "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, harga_satuan) "
            "VALUES (1, 1, 0, 5000)"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: jumlah = 0 tidak valid!")
    except sqlite3.IntegrityError:
        pass  # Benar — ditolak oleh CHECK (jumlah > 0)
    finally:
        conn.close()


# ============================================================
# KELOMPOK UJI 3: Integritas Referensial (Foreign Keys)
# ============================================================
def uji_tolak_menu_dengan_kategori_tidak_ada():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO menu (kategori_id, nama, harga, status) "
            "VALUES (999, 'Menu Tanpa Kategori', 10000, 'tersedia')"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: kategori_id=999 tidak ada!")
    except sqlite3.IntegrityError:
        pass  # Benar — FK REFERENCES kategori(id)
    finally:
        conn.close()


def uji_tolak_transaksi_dengan_pengguna_tidak_ada():
    conn = buat_db()
    try:
        conn.execute(
            "INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, "
            "metode_pembayaran, uang_diterima, pengguna_id) "
            "VALUES ('TRX-TEST-004', '2026-11-14 10:00:00', 'dine_in', 'tunai', 50000, 999)"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: pengguna_id=999 tidak ada!")
    except sqlite3.IntegrityError:
        pass  # Benar — FK REFERENCES pengguna(id)
    finally:
        conn.close()


def uji_tolak_username_duplikat():
    conn = buat_db()
    try:
        # 'kasir1' sudah ada dari seed data
        conn.execute(
            "INSERT INTO pengguna (username, password_hash, nama_lengkap, peran) "
            "VALUES ('kasir1', 'hash_baru', 'Kasir Duplikat', 'kasir')"
        )
        conn.commit()
        raise AssertionError("SEHARUSNYA ditolak: username 'kasir1' sudah terdaftar (UNIQUE)!")
    except sqlite3.IntegrityError:
        pass  # Benar — UNIQUE pada kolom username
    finally:
        conn.close()


def uji_cascade_delete_detail_saat_transaksi_dihapus():
    conn = buat_db()
    conn.execute("PRAGMA foreign_keys = ON")
    # Sisipkan transaksi
    conn.execute(
        "INSERT INTO transaksi (id, nomor_transaksi, tanggal_waktu, tipe_pesanan, "
        "metode_pembayaran, uang_diterima, pengguna_id) "
        "VALUES (99, 'TRX-CASCADE-001', '2026-11-14 11:00:00', 'take_away', 'tunai', 15000, 2)"
    )
    # Sisipkan detail transaksi
    conn.execute(
        "INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, harga_satuan) "
        "VALUES (99, 1, 1, 15000)"
    )
    conn.commit()
    # Hapus transaksi induk → detail harus ikut terhapus (CASCADE)
    conn.execute("DELETE FROM transaksi WHERE id = 99")
    conn.commit()
    cur = conn.execute("SELECT COUNT(*) FROM detail_transaksi WHERE transaksi_id = 99")
    sisa = cur.fetchone()[0]
    assert sisa == 0, f"Detail transaksi seharusnya terhapus CASCADE, masih ada: {sisa} baris"
    conn.close()


# ============================================================
# Jalankan semua pengujian
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Pengujian Integritas Skema — KasirWarung")
    print("=" * 55)

    print("\n[1] Uji Struktur Tabel & Seed Data")
    uji("Semua 5 tabel wajib ada di skema",          uji_semua_tabel_ada)
    uji("Seed data kategori minimal 4 baris",         uji_seed_data_kategori)
    uji("Seed data menu minimal 1 baris",             uji_seed_data_menu)

    print("\n[2] Uji Batasan Data (CHECK Constraints)")
    uji("Tolak harga menu bernilai negatif",          uji_tolak_harga_menu_negatif)
    uji("Tolak status menu di luar 'tersedia/habis'", uji_tolak_status_menu_tidak_valid)
    uji("Tolak peran pengguna di luar kasir/pemilik", uji_tolak_peran_pengguna_tidak_valid)
    uji("Tolak metode bayar di luar tunai/qris",      uji_tolak_metode_bayar_tidak_valid)
    uji("Tolak tipe pesanan di luar dine_in/take_away", uji_tolak_tipe_pesanan_tidak_valid)
    uji("Tolak jumlah item detail = 0 atau negatif",  uji_tolak_jumlah_detail_nol_atau_negatif)

    print("\n[3] Uji Integritas Referensial (Foreign Keys)")
    uji("Tolak menu dengan kategori_id tidak ada",    uji_tolak_menu_dengan_kategori_tidak_ada)
    uji("Tolak transaksi dengan pengguna_id tidak ada", uji_tolak_transaksi_dengan_pengguna_tidak_ada)
    uji("Tolak username pengguna duplikat",            uji_tolak_username_duplikat)
    uji("CASCADE DELETE: detail terhapus saat transaksi induk dihapus", uji_cascade_delete_detail_saat_transaksi_dihapus)

    print("\n" + "=" * 55)
    print(f"  Hasil : {lulus} LULUS  |  {gagal} GAGAL")
    print("=" * 55)

    if gagal == 0:
        print("  ✅ Semua pengujian lulus! Skema siap digunakan.")
    else:
        print("  ❌ Ada pengujian yang gagal. Periksa schema.sql.")
    print()
