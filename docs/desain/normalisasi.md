# Normalisasi Basis Data — Kasir Warung Makan (KasirWarung)
## Langkah 6 Sesi 1: Normalisasi 1NF → 2NF → 3NF (Jobsheet 6)

---

## A. Sampel Dokumen Fisik: Nota Transaksi Warung Makan

Berikut adalah contoh nota transaksi nyata yang ditulis tangan oleh kasir warung makan saat jam makan siang:

```
========================================
        WARUNG MAKAN BAROKAH
        Jl. Ahmad Yani No. 12, Sampit
========================================
No. Nota  : TRX-20261114-003
Tanggal   : 14 November 2026 — 12.35 WIB
Kasir     : Siti (Kasir)
Meja      : 05
Tipe      : Makan di Tempat (Dine-in)
----------------------------------------
No  Nama Menu         Qty  Harga  Subtotal
1   Nasi Putih        2    5000   10000
2   Ayam Goreng       2    15000  30000
3   Sayur Bayam       1    8000   8000
4   Es Teh Manis      2    5000   10000
----------------------------------------
Total Bayar           :   Rp 58.000
Uang Diterima         :   Rp 60.000
Kembalian             :   Rp  2.000
Metode Pembayaran     :   Tunai
========================================
       Terima kasih atas kunjungan Anda!
========================================
```

---

## B. Tabel Awal (Unnormalized Form / UNF)

Semua data dari nota di atas dimasukkan ke dalam satu tabel datar tanpa aturan normalisasi:

| id_nota | tanggal_waktu | kasir_username | kasir_nama | kasir_peran | tipe_pesanan | nomor_meja | metode_pembayaran | uang_diterima | nama_menu_1 | qty_1 | harga_1 | nama_menu_2 | qty_2 | harga_2 | nama_menu_3 | qty_3 | harga_3 | nama_menu_4 | qty_4 | harga_4 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 | Nasi Putih | 2 | 5000 | Ayam Goreng | 2 | 15000 | Sayur Bayam | 1 | 8000 | Es Teh Manis | 2 | 5000 |

**Masalah UNF:**
- Kolom berulang: `nama_menu_1`, `nama_menu_2`, dst. → tabel ini tidak akan bisa menampung pesanan ke-5, ke-6, dsb. tanpa menambah kolom baru.
- Data tidak atomik per sel.
- Banyak kolom `NULL` jika menu yang dipesan lebih sedikit.

---

## C. Bentuk Normal Pertama — 1NF (*First Normal Form*)

### Aturan 1NF:
1. Setiap sel harus berisi **satu nilai atomik** (tidak ada daftar atau kolom berulang).
2. Setiap baris harus unik (memiliki kunci yang membedakannya).

### Langkah:
Pecah kolom berulang (`nama_menu_1`, `qty_1`, `harga_1`, dst.) menjadi baris terpisah. Setiap baris mewakili satu item menu dalam satu nota transaksi.

**Tabel setelah 1NF:**

| id_nota | tanggal_waktu | kasir_username | kasir_nama | kasir_peran | tipe_pesanan | nomor_meja | metode_pembayaran | uang_diterima | nama_menu | qty | harga_satuan |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 | Nasi Putih | 2 | 5000 |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 | Ayam Goreng | 2 | 15000 |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 | Sayur Bayam | 1 | 8000 |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 | Es Teh Manis | 2 | 5000 |

**Kunci Komposit 1NF:** (`id_nota`, `nama_menu`)

**Masalah yang Masih Ada:**
- Data `tanggal_waktu`, `kasir_username`, `kasir_nama`, `kasir_peran`, `tipe_pesanan`, `nomor_meja`, `metode_pembayaran`, `uang_diterima` **diulang** di setiap baris → ini adalah redundansi akibat ketergantungan parsial, yang diselesaikan di 2NF.

---

## D. Bentuk Normal Kedua — 2NF (*Second Normal Form*)

### Aturan 2NF:
1. Harus sudah memenuhi 1NF.
2. Setiap kolom non-kunci harus bergantung **penuh** pada seluruh kunci komposit, bukan hanya sebagian.

### Langkah:
Identifikasi ketergantungan parsial pada kunci komposit (`id_nota`, `nama_menu`):

| Kolom | Bergantung pada `id_nota` saja? | Bergantung pada `nama_menu` saja? | Bergantung penuh pada keduanya? |
| :--- | :---: | :---: | :---: |
| `tanggal_waktu` | ✅ Ya | ❌ | ❌ |
| `kasir_username` | ✅ Ya | ❌ | ❌ |
| `kasir_nama` | ✅ Ya | ❌ | ❌ |
| `kasir_peran` | ✅ Ya | ❌ | ❌ |
| `tipe_pesanan` | ✅ Ya | ❌ | ❌ |
| `nomor_meja` | ✅ Ya | ❌ | ❌ |
| `metode_pembayaran` | ✅ Ya | ❌ | ❌ |
| `uang_diterima` | ✅ Ya | ❌ | ❌ |
| `qty` | ❌ | ❌ | ✅ Ya (berbeda per transaksi) |
| `harga_satuan` | ❌ | ❌ | ✅ Ya (harga saat itu) |

**Pemisahan ke dua tabel:**

**Tabel `transaksi`** ← kolom yang bergantung pada `id_nota` saja:

| id_nota | tanggal_waktu | kasir_username | kasir_nama | kasir_peran | tipe_pesanan | nomor_meja | metode_pembayaran | uang_diterima |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | Siti | kasir | dine_in | 05 | tunai | 60000 |

**Tabel `detail_transaksi`** ← kolom yang bergantung penuh pada kunci komposit:

| id_nota | nama_menu | qty | harga_satuan |
| :---: | :---: | :---: | :---: |
| TRX-20261114-003 | Nasi Putih | 2 | 5000 |
| TRX-20261114-003 | Ayam Goreng | 2 | 15000 |
| TRX-20261114-003 | Sayur Bayam | 1 | 8000 |
| TRX-20261114-003 | Es Teh Manis | 2 | 5000 |

**Masalah yang Masih Ada pada Tabel `transaksi`:**
- `kasir_nama` dan `kasir_peran` bergantung pada `kasir_username`, bukan pada `id_nota` → ini adalah ketergantungan transitif, yang diselesaikan di 3NF.

---

## E. Bentuk Normal Ketiga — 3NF (*Third Normal Form*)

### Aturan 3NF:
1. Harus sudah memenuhi 2NF.
2. Tidak boleh ada **ketergantungan transitif** (kolom non-kunci tidak boleh bergantung pada kolom non-kunci lain).

### Langkah:
Identifikasi ketergantungan transitif pada tabel `transaksi`:

> `id_nota` → `kasir_username` → `kasir_nama` dan `kasir_peran`

Artinya: `kasir_nama` dan `kasir_peran` tidak langsung bergantung pada `id_nota`, melainkan bergantung pada `kasir_username`. Ini adalah pelanggaran 3NF.

**Pemisahan ke tabel baru `pengguna`:**

**Tabel `pengguna`** ← data kasir yang berdiri sendiri:

| username | nama_lengkap | peran |
| :---: | :---: | :---: |
| siti | Siti | kasir |

**Tabel `transaksi`** ← setelah 3NF (kolom `kasir_nama` dan `kasir_peran` dihapus, cukup menyimpan `kasir_username` sebagai FK):

| id_nota | tanggal_waktu | kasir_username (FK) | tipe_pesanan | nomor_meja | metode_pembayaran | uang_diterima |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TRX-20261114-003 | 2026-11-14 12:35:00 | siti | dine_in | 05 | tunai | 60000 |

---

## F. Ringkasan Tahapan Normalisasi

| Tahap | Masalah yang Diatasi | Tindakan | Tabel Dihasilkan |
| :---: | :--- | :--- | :--- |
| **UNF** | Kolom berulang per item menu | — | 1 tabel datar (tidak valid) |
| **1NF** | Kolom berulang → data tidak atomik | Pecah kolom berulang menjadi baris terpisah | 1 tabel dengan kunci komposit |
| **2NF** | Ketergantungan parsial pada kunci komposit | Pisahkan kolom yang hanya bergantung sebagian | `transaksi` + `detail_transaksi` |
| **3NF** | Ketergantungan transitif (`username` → `nama` & `peran`) | Pisahkan data kasir ke tabel mandiri | `transaksi` + `detail_transaksi` + `pengguna` |

---

## G. Pemetaan Hasil 3NF ke ERD Final

Hasil normalisasi ini sepenuhnya konsisten dengan ERD yang telah dirancang pada Langkah 5:
- Tabel `pengguna` ↔ entitas `PENGGUNA`
- Tabel `transaksi` ↔ entitas `TRANSAKSI`
- Tabel `detail_transaksi` ↔ entitas `DETAIL_TRANSAKSI`
- Tabel `menu` (data master menu terpisah, bukan dari kolom `nama_menu`) ↔ entitas `MENU`
- Tabel `kategori` (pengelompokan menu terpisah) ↔ entitas `KATEGORI`
