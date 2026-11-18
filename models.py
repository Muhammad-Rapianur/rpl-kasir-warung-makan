import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Jalur berkas basis data SQLite dan skema DDL
DB_PATH = Path(__file__).with_name("kasir_warung.db")
SCHEMA_PATH = Path(__file__).parent / "docs" / "desain" / "schema.sql"


@contextmanager
def koneksi():
    """Buka koneksi SQLite, aktifkan kunci asing (foreign keys),

    gunakan row_factory Row, lalu commit dan tutup secara aman.
    """
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def init_db():
    """Inisialisasi basis data dari schema.sql jika kasir_warung.db belum ada."""
    if not DB_PATH.exists():
        if not SCHEMA_PATH.exists():
            raise FileNotFoundError(f"Berkas skema tidak ditemukan di {SCHEMA_PATH}")
        with koneksi() as db:
            db.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def semua_menu():
    """Mengambil seluruh daftar menu beserta nama kategorinya, diurutkan berdasarkan nama."""
    with koneksi() as db:
        return db.execute(
            """
            SELECT m.id, m.nama, m.harga, m.status, m.kategori_id, k.nama AS nama_kategori
            FROM menu m
            JOIN kategori k ON m.kategori_id = k.id
            ORDER BY m.nama ASC
            """
        ).fetchall()


def semua_kategori():
    """Mengambil seluruh kategori untuk pilihan dropdown form."""
    with koneksi() as db:
        return db.execute("SELECT id, nama FROM kategori ORDER BY nama ASC").fetchall()


def semua_kategori_detail():
    """Mengambil seluruh kategori beserta jumlah menu terkait (untuk halaman daftar kategori)."""
    with koneksi() as db:
        return db.execute(
            """
            SELECT k.id, k.nama, COUNT(m.id) AS jumlah_menu
            FROM kategori k
            LEFT JOIN menu m ON k.id = m.kategori_id
            GROUP BY k.id, k.nama
            ORDER BY k.nama ASC
            """
        ).fetchall()


def ambil_kategori(kategori_id):
    """Mengambil satu data kategori berdasarkan id."""
    with koneksi() as db:
        return db.execute(
            "SELECT id, nama FROM kategori WHERE id = ?", (kategori_id,)
        ).fetchone()


def tambah_kategori(nama):
    """Menambahkan kategori hidangan baru."""
    with koneksi() as db:
        db.execute("INSERT INTO kategori (nama) VALUES (?)", (nama,))


def ubah_kategori(kategori_id, nama):
    """Memperbarui nama kategori berdasarkan id."""
    with koneksi() as db:
        db.execute(
            "UPDATE kategori SET nama = ? WHERE id = ?", (nama, kategori_id)
        )


def hapus_kategori(kategori_id):
    """Menghapus kategori berdasarkan id.

    Memicu sqlite3.IntegrityError jika masih ada menu yang menggunakannya.
    """
    with koneksi() as db:
        db.execute("DELETE FROM kategori WHERE id = ?", (kategori_id,))


# ============================================================
# Modul Transaksi & Detail Transaksi (Jobsheet 10)
# ============================================================

def semua_transaksi():
    """Mengambil seluruh data transaksi penjualan beserta nama kasir (JOIN pengguna),

    total tagihan agregasi (SUM detail_transaksi), dan rincian menu yang dipesan.
    """
    with koneksi() as db:
        return db.execute(
            """
            SELECT 
                t.id,
                t.nomor_transaksi,
                t.tanggal_waktu,
                t.tipe_pesanan,
                t.nomor_meja,
                t.metode_pembayaran,
                t.uang_diterima,
                p.nama_lengkap AS nama_kasir,
                COALESCE(SUM(d.jumlah * d.harga_satuan), 0) AS total_belanja,
                COALESCE(GROUP_CONCAT(m.nama || ' (' || d.jumlah || 'x)', ', '), '-') AS rincian_menu
            FROM transaksi t
            JOIN pengguna p ON t.pengguna_id = p.id
            LEFT JOIN detail_transaksi d ON t.id = d.transaksi_id
            LEFT JOIN menu m ON d.menu_id = m.id
            GROUP BY 
                t.id, t.nomor_transaksi, t.tanggal_waktu, t.tipe_pesanan,
                t.nomor_meja, t.metode_pembayaran, t.uang_diterima, p.nama_lengkap
            ORDER BY t.tanggal_waktu DESC, t.id DESC
            """
        ).fetchall()




def tambah_menu(nama, kategori_id, harga, status="tersedia"):
    """Menambahkan menu hidangan baru ke dalam basis data SQLite."""
    with koneksi() as db:
        db.execute(
            "INSERT INTO menu (nama, kategori_id, harga, status) VALUES (?, ?, ?, ?)",
            (nama, kategori_id, harga, status),
        )


def ambil_menu(menu_id):
    """Mengambil satu data menu berdasarkan id. Mengembalikan None jika tidak ditemukan."""
    with koneksi() as db:
        return db.execute(
            "SELECT id, nama, kategori_id, harga, status FROM menu WHERE id = ?",
            (menu_id,),
        ).fetchone()


def ubah_menu(menu_id, nama, kategori_id, harga, status="tersedia"):
    """Memperbarui data menu berdasarkan id."""
    with koneksi() as db:
        db.execute(
            """
            UPDATE menu
            SET nama = ?, kategori_id = ?, harga = ?, status = ?
            WHERE id = ?
            """,
            (nama, kategori_id, harga, status, menu_id),
        )


def hapus_menu(menu_id):
    """Menghapus menu berdasarkan id.

    Memicu sqlite3.IntegrityError jika menu dirujuk oleh tabel detail_transaksi.
    """
    with koneksi() as db:
        db.execute("DELETE FROM menu WHERE id = ?", (menu_id,))




