-- ============================================================
-- schema.sql
-- Skema Basis Data Sistem Kasir Warung Makan (KasirWarung)
-- Mata Kuliah : Rekayasa Perangkat Lunak (RPL)
-- Jobsheet    : 6 — Sesi 2, Langkah 8
-- Engine      : SQLite 3
-- Encoding    : UTF-8
-- ============================================================

-- Aktifkan pengecekan Foreign Key (wajib di SQLite)
PRAGMA foreign_keys = ON;

-- ============================================================
-- Hapus tabel lama jika ada (urutan terbalik dari FK)
-- ============================================================
DROP TABLE IF EXISTS detail_transaksi;
DROP TABLE IF EXISTS transaksi;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS kategori;
DROP TABLE IF EXISTS pengguna;

-- ============================================================
-- Tabel 1: pengguna
-- Menyimpan akun kasir dan pemilik warung makan.
-- Sumber KF : UC-01 (Login), KNF-06 (Keamanan Akun)
-- ============================================================
CREATE TABLE pengguna (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    password_hash TEXT    NOT NULL,
    nama_lengkap  TEXT    NOT NULL,
    peran         TEXT    NOT NULL
        CHECK (peran IN ('kasir', 'pemilik'))
);

-- ============================================================
-- Tabel 2: kategori
-- Menyimpan kelompok menu (Makanan, Minuman, Lauk, Ekstra).
-- Sumber KF : KF-01 (Katalog Menu Berdasarkan Kategori)
-- ============================================================
CREATE TABLE kategori (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT    NOT NULL UNIQUE
);

-- ============================================================
-- Tabel 3: menu
-- Menyimpan daftar makanan dan minuman yang dijual.
-- Sumber KF : KF-01, KF-02, KF-05
-- ============================================================
CREATE TABLE menu (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kategori_id INTEGER NOT NULL,
    nama        TEXT    NOT NULL UNIQUE,
    harga       INTEGER NOT NULL
        CHECK (harga >= 0),
    status      TEXT    NOT NULL DEFAULT 'tersedia'
        CHECK (status IN ('tersedia', 'habis')),
    FOREIGN KEY (kategori_id) REFERENCES kategori (id)
);

-- ============================================================
-- Tabel 4: transaksi
-- Menyimpan data kepala (header) setiap transaksi penjualan.
-- Sumber KF : KF-03, KF-06, KF-07, KF-08, KF-09, KF-11, KF-12
-- ============================================================
CREATE TABLE transaksi (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    nomor_transaksi    TEXT    NOT NULL UNIQUE,
    tanggal_waktu      TEXT    NOT NULL,   -- Format ISO: 'YYYY-MM-DD HH:MM:SS'
    tipe_pesanan       TEXT    NOT NULL
        CHECK (tipe_pesanan IN ('dine_in', 'take_away')),
    nomor_meja         TEXT,               -- NULL jika tipe_pesanan = 'take_away'
    metode_pembayaran  TEXT    NOT NULL
        CHECK (metode_pembayaran IN ('tunai', 'qris')),
    uang_diterima      INTEGER NOT NULL
        CHECK (uang_diterima >= 0),
    pengguna_id        INTEGER NOT NULL,
    FOREIGN KEY (pengguna_id) REFERENCES pengguna (id)
);

-- ============================================================
-- Tabel 5: detail_transaksi
-- Tabel penghubung (junction table) antara transaksi dan menu.
-- Menyimpan rincian item pesanan per transaksi.
-- Sumber KF : KF-04, KF-09, KF-13
-- ============================================================
CREATE TABLE detail_transaksi (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    transaksi_id  INTEGER NOT NULL,
    menu_id       INTEGER NOT NULL,
    jumlah        INTEGER NOT NULL
        CHECK (jumlah > 0),
    harga_satuan  INTEGER NOT NULL
        CHECK (harga_satuan >= 0),
    catatan       TEXT,                    -- NULL jika tidak ada catatan khusus
    FOREIGN KEY (transaksi_id) REFERENCES transaksi (id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id)      REFERENCES menu (id)
);

-- ============================================================
-- Indeks untuk mempercepat kueri yang sering dijalankan
-- ============================================================

-- Mempercepat pencarian riwayat transaksi berdasarkan tanggal
CREATE INDEX idx_transaksi_tanggal
    ON transaksi (tanggal_waktu);

-- Mempercepat rekap transaksi per kasir
CREATE INDEX idx_transaksi_pengguna
    ON transaksi (pengguna_id);

-- Mempercepat kueri menu terlaris (GROUP BY menu_id di detail)
CREATE INDEX idx_detail_menu
    ON detail_transaksi (menu_id);

-- Mempercepat JOIN detail per transaksi
CREATE INDEX idx_detail_transaksi
    ON detail_transaksi (transaksi_id);

-- ============================================================
-- Data awal (Seed Data) — kategori default warung makan
-- ============================================================
INSERT INTO kategori (nama) VALUES
    ('Makanan Utama'),
    ('Sayur & Lauk Pauk'),
    ('Minuman'),
    ('Ekstra & Camilan');

-- ============================================================
-- Data awal (Seed Data) — akun pengguna default
-- Password: 'admin123' (hash bcrypt — ganti saat production)
-- ============================================================
INSERT INTO pengguna (username, password_hash, nama_lengkap, peran) VALUES
    ('pemilik', 'HASH_DIGANTI_SAAT_SETUP', 'Pemilik Warung', 'pemilik'),
    ('kasir1',  'HASH_DIGANTI_SAAT_SETUP', 'Kasir Utama',   'kasir');

-- ============================================================
-- Data awal (Seed Data) — contoh menu warung makan
-- ============================================================
INSERT INTO menu (kategori_id, nama, harga, status) VALUES
    -- Makanan Utama (id=1)
    (1, 'Nasi Putih',       4000,  'tersedia'),
    (1, 'Nasi Goreng',      15000, 'tersedia'),
    -- Sayur & Lauk Pauk (id=2)
    (2, 'Ayam Goreng',      15000, 'tersedia'),
    (2, 'Ayam Bakar',       18000, 'tersedia'),
    (2, 'Ikan Goreng',      12000, 'tersedia'),
    (2, 'Tempe Goreng',     3000,  'tersedia'),
    (2, 'Tahu Goreng',      3000,  'tersedia'),
    (2, 'Sayur Bayam',      5000,  'tersedia'),
    (2, 'Sayur Asem',       5000,  'tersedia'),
    -- Minuman (id=3)
    (3, 'Es Teh Manis',     5000,  'tersedia'),
    (3, 'Es Jeruk',         7000,  'tersedia'),
    (3, 'Air Putih',        3000,  'tersedia'),
    -- Ekstra & Camilan (id=4)
    (4, 'Kerupuk',          2000,  'tersedia'),
    (4, 'Sambal Ekstra',    2000,  'tersedia');
