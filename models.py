import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Jalur berkas basis data SQLite dan skema DDL
DB_PATH = Path(os.environ.get("KASIR_DB") or os.environ.get("TOKO_DB") or Path(__file__).with_name("kasir_warung.db"))
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


def _escape_like(teks):
    """Netralkan karakter % dan _ agar dicari secara harfiah sebagai teks biasa."""
    return teks.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def cari_menu(kata="", kategori_id=None, status=None):
    """Daftar menu dengan pencarian nama aman (LIKE ? ESCAPE '\\') dan penyaringan (Langkah 9 & 10)."""
    sql = """
        SELECT m.id, m.nama, m.harga, m.status, m.kategori_id, k.nama AS nama_kategori
        FROM menu m
        JOIN kategori k ON m.kategori_id = k.id
        WHERE m.nama LIKE ? ESCAPE '\\'
    """
    param = ["%" + _escape_like(kata) + "%"]

    if kategori_id:
        sql += " AND m.kategori_id = ?"
        param.append(kategori_id)

    if status and status in ("tersedia", "habis"):
        sql += " AND m.status = ?"
        param.append(status)

    sql += " ORDER BY m.nama ASC"

    with koneksi() as db:
        return db.execute(sql, param).fetchall()


def semua_menu():
    """Mengambil seluruh daftar menu beserta nama kategorinya, diurutkan berdasarkan nama."""
    return cari_menu()


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


def tambah_transaksi_dengan_detail(
    menu_id,
    jumlah,
    tanggal_waktu,
    tipe_pesanan,
    nomor_meja,
    metode_pembayaran,
    uang_diterima,
    pengguna_id=2,
    items=None,
):
    """Menyimpan data kepala transaksi DAN rincian pesanan (bisa multi-item) dalam SATU transaksi atomik SQLite.

    (Jobsheet 10 - Langkah 5: Transaksi multi-tabel dalam satu with koneksi()).
    Mendukung item tunggal (menu_id & jumlah) maupun multi-item via parameter items=[{'menu_id': .., 'jumlah': ..}].
    """
    with koneksi() as db:
        # Siapkan daftar item yang akan dimasukkan
        daftar_item = []
        if items and isinstance(items, list) and len(items) > 0:
            for itm in items:
                m_id = int(itm["menu_id"])
                jml = int(itm["jumlah"])
                menu = db.execute("SELECT id, nama, harga, status FROM menu WHERE id = ?", (m_id,)).fetchone()
                if menu is None:
                    raise sqlite3.IntegrityError(f"Menu dengan ID {m_id} tidak ditemukan.")
                daftar_item.append({"menu_id": m_id, "jumlah": jml, "harga": menu["harga"]})
        else:
            # Fallback untuk pengujian unit tunggal
            menu = db.execute("SELECT id, nama, harga, status FROM menu WHERE id = ?", (menu_id,)).fetchone()
            if menu is None:
                raise sqlite3.IntegrityError(f"Menu dengan ID {menu_id} tidak ditemukan.")
            daftar_item.append({"menu_id": int(menu_id), "jumlah": int(jumlah), "harga": menu["harga"]})

        # 2. Generate nomor transaksi unik berformat TRX-YYYYMMDD-XXX
        tgl_str = (
            tanggal_waktu[:10].replace("-", "")
            if tanggal_waktu and len(tanggal_waktu) >= 10
            else "20261119"
        )
        total_hari_ini = db.execute(
            "SELECT COUNT(*) FROM transaksi WHERE nomor_transaksi LIKE ?",
            (f"TRX-{tgl_str}-%",),
        ).fetchone()[0]
        nomor_transaksi = f"TRX-{tgl_str}-{total_hari_ini + 1:03d}"

        # 3. Masukkan transaksi header (hanya tunai)
        cursor = db.execute(
            """
            INSERT INTO transaksi (nomor_transaksi, tanggal_waktu, tipe_pesanan, nomor_meja, metode_pembayaran, uang_diterima, pengguna_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                nomor_transaksi,
                tanggal_waktu,
                tipe_pesanan,
                nomor_meja,
                "tunai",
                uang_diterima,
                pengguna_id,
            ),
        )
        trx_id = cursor.lastrowid

        # 4. Masukkan seluruh baris detail_transaksi multi-item
        for itm in daftar_item:
            db.execute(
                """
                INSERT INTO detail_transaksi (transaksi_id, menu_id, jumlah, harga_satuan)
                VALUES (?, ?, ?, ?)
                """,
                (trx_id, itm["menu_id"], itm["jumlah"], itm["harga"]),
            )
        return nomor_transaksi





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


# ============================================================
# Modul Pengguna & Autentikasi (Jobsheet 11)
# ============================================================

def ambil_pengguna(pengguna_id):
    """Mengambil satu data pengguna berdasarkan id."""
    with koneksi() as db:
        return db.execute(
            "SELECT id, username, password_hash, nama_lengkap, peran FROM pengguna WHERE id = ?",
            (pengguna_id,),
        ).fetchone()


def cari_pengguna(username):
    """Mencari satu data pengguna berdasarkan username persis."""
    with koneksi() as db:
        return db.execute(
            "SELECT id, username, password_hash, nama_lengkap, peran FROM pengguna WHERE username = ?",
            ((username or "").strip(),),
        ).fetchone()


def tambah_pengguna(username, password_hash, nama_lengkap, peran):
    """Menambahkan akun pengguna baru dengan password yang telah di-hash secara aman."""
    with koneksi() as db:
        cursor = db.execute(
            """
            INSERT INTO pengguna (username, password_hash, nama_lengkap, peran)
            VALUES (?, ?, ?, ?)
            """,
            (username.strip(), password_hash, nama_lengkap.strip(), peran.strip()),
        )
        return cursor.lastrowid


def perbarui_password_pengguna(pengguna_id, password_hash):
    """Memperbarui hash password pengguna berdasarkan ID."""
    with koneksi() as db:
        db.execute(
            "UPDATE pengguna SET password_hash = ? WHERE id = ?",
            (password_hash, pengguna_id),
        )


def rekapitulasi_omzet(tanggal_mulai=None, tanggal_selesai=None):
    """Menghitung agregasi omzet total, jumlah nota, dan 5 menu terlaris (wf-06)."""
    with koneksi() as db:
        sql_summary = """
            SELECT 
                COALESCE(SUM(d.jumlah * d.harga_satuan), 0) AS total_omzet,
                COUNT(DISTINCT t.id) AS total_nota
            FROM transaksi t
            JOIN detail_transaksi d ON t.id = d.transaksi_id
        """
        ringkasan = db.execute(sql_summary).fetchone()

        sql_terlaris = """
            SELECT 
                m.nama AS nama_menu,
                k.nama AS nama_kategori,
                COALESCE(SUM(d.jumlah), 0) AS porsi_terjual,
                COALESCE(SUM(d.jumlah * d.harga_satuan), 0) AS total_akumulasi
            FROM detail_transaksi d
            JOIN menu m ON d.menu_id = m.id
            JOIN kategori k ON m.kategori_id = k.id
            GROUP BY m.id, m.nama, k.nama
            ORDER BY porsi_terjual DESC, total_akumulasi DESC
            LIMIT 5
        """
        terlaris = db.execute(sql_terlaris).fetchall()

        return dict(ringkasan), [dict(row) for row in terlaris]






