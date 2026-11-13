# Kamus Data (Data Dictionary) — Kasir Warung Makan (KasirWarung)
## Dokumen Perancangan Basis Data (Jobsheet 6)

Dokumen ini memuat kamus data formal untuk seluruh tabel basis data SQLite pada sistem kasir warung makan, disusun berdasarkan format baku Lampiran C.2 Jobsheet 6.

---

### 1. Tabel: `pengguna`
*Deskripsi:* Menyimpan data akun kasir dan pemilik warung makan untuk keperluan otentikasi login dan identifikasi kasir yang memproses pesanan.  
*Sumber Kebutuhan:* UC-01, NFR-06

| Kolom | Tipe Data | Wajib | Kunci | Aturan Nilai / Batasan | Sumber |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`), pengenal unik pengguna | — |
| `username` | TEXT | Ya | UK | Unik, tidak boleh kosong, tidak boleh ada spasi | UC-01 |
| `password_hash` | TEXT | Ya | — | Berupa hash string aman (bukan plain text) | NFR-06 |
| `nama_lengkap` | TEXT | Ya | — | Nama kasir/pemilik untuk dicantumkan di struk | KF-03 |
| `peran` | TEXT | Ya | — | Dibatasi: `CHECK (peran IN ('kasir', 'pemilik'))` | UC-01 |

---

### 2. Tabel: `kategori`
*Deskripsi:* Menyimpan data klasifikasi/kelompok menu makanan dan minuman.  
*Sumber Kebutuhan:* KF-01, UC-05

| Kolom | Tipe Data | Wajib | Kunci | Aturan Nilai / Batasan | Sumber |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`), pengenal unik kategori | — |
| `nama` | TEXT | Ya | UK | Unik (misal: Makanan Utama, Sayur & Lauk, Minuman, Ekstra) | KF-01 |

---

### 3. Tabel: `menu`
*Deskripsi:* Menyimpan master data makanan dan minuman yang dijual beserta harga dan status ketersediaan harian.  
*Sumber Kebutuhan:* KF-01, KF-02, KF-05, UC-02, UC-05

| Kolom | Tipe Data | Wajib | Kunci | Aturan Nilai / Batasan | Sumber |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`), pengenal unik menu | — |
| `kategori_id` | INTEGER | Ya | FK | Merujuk ke `kategori(id)` | KF-01 |
| `nama` | TEXT | Ya | UK | Unik, nama masakan/minuman (misal: Ayam Goreng) | KF-01 |
| `harga` | INTEGER | Ya | — | $\ge 0$, rupiah tanpa desimal, `CHECK (harga >= 0)` | KF-02 |
| `status` | TEXT | Ya | — | Dibatasi: `CHECK (status IN ('tersedia', 'habis'))`, default: `'tersedia'` | KF-05 |

---

### 4. Tabel: `transaksi`
*Deskripsi:* Menyimpan data kepala (*header*) transaksi penjualan yang berhasil diselesaikan di kasir.  
*Sumber Kebutuhan:* KF-03, KF-06, KF-07, KF-08, KF-09, KF-11, KF-12, UC-02, UC-06, UC-07

| Kolom | Tipe Data | Wajib | Kunci | Aturan Nilai / Batasan | Sumber |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`), pengenal unik transaksi | — |
| `nomor_transaksi` | TEXT | Ya | UK | Unik, format penomoran harian: `TRX-YYYYMMDD-XXX` | KF-09 |
| `tanggal_waktu` | TEXT | Ya | — | Format standar ISO: `YYYY-MM-DD HH:MM:SS` | KF-09 |
| `tipe_pesanan` | TEXT | Ya | — | Dibatasi: `CHECK (tipe_pesanan IN ('dine_in', 'take_away'))` | KF-03 |
| `nomor_meja` | TEXT | Tidak | — | Nomor/teks meja. Boleh `NULL` jika `tipe_pesanan = 'take_away'` | KF-03 |
| `metode_pembayaran`| TEXT | Ya | — | Dibatasi: `CHECK (metode_pembayaran IN ('tunai', 'qris'))` | KF-08 |
| `uang_diterima` | INTEGER | Ya | — | $\ge 0$, nominal uang kasir, `CHECK (uang_diterima >= 0)` | KF-06 |
| `pengguna_id` | INTEGER | Ya | FK | Merujuk ke `pengguna(id)` kasir yang memproses nota | UC-02 |

*Catatan:* Kolom `total_bayar` dan `kembalian` sengaja **tidak dibuat** karena merupakan nilai turunan matematis yang dihitung saat kueri (`SUM`).

---

### 5. Tabel: `detail_transaksi`
*Deskripsi:* Tabel penghubung (*junction table*) antara `transaksi` dan `menu` yang memuat rincian setiap item menu yang dipesan.  
*Sumber Kebutuhan:* KF-04, KF-09, KF-13, UC-02

| Kolom | Tipe Data | Wajib | Kunci | Aturan Nilai / Batasan | Sumber |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `id` | INTEGER | Ya | PK | Otomatis (`AUTOINCREMENT`), pengenal unik detail | — |
| `transaksi_id` | INTEGER | Ya | FK | Merujuk ke `transaksi(id)` dengan `ON DELETE CASCADE` | KF-09 |
| `menu_id` | INTEGER | Ya | FK | Merujuk ke `menu(id)` | KF-04 |
| `jumlah` | INTEGER | Ya | — | Porsi pesanan $> 0$, `CHECK (jumlah > 0)` | KF-04 |
| `harga_satuan` | INTEGER | Ya | — | $\ge 0$, harga saat transaksi, `CHECK (harga_satuan >= 0)` | KF-04 |
| `catatan` | TEXT | Tidak | — | Catatan khusus pesanan (misal: "tanpa sambal"), boleh `NULL` | KF-04 |
