# Relasi dan Kardinalitas Sistem — Kasir Warung Makan (KasirWarung)
## Langkah 4 Sesi 1: Perancangan Basis Data (Jobsheet 6)

Dokumen ini memuat perincian relasi antarentitas, kalimat pembacaan dua arah, kardinalitas (*crow's foot*), penempatan kunci asing (*Foreign Key*), serta resolusi relasi banyak-ke-banyak (*many-to-many*) untuk **Sistem Kasir Warung Makan (*KasirWarung*)**.

---

## 1. Tabel Relasi dan Kardinalitas Dua Arah (Sesuai Format Langkah 4 Jobsheet 6)

| No | Entitas A — Relasi — Entitas B | Kalimat Dua Arah (Uji Konsistensi) | Kardinalitas | Letak Kunci Asing (FK) |
| :-: | :--- | :--- | :---: | :--- |
| **1** | **`pengguna`** — mencatat — **`transaksi`** | • Satu `pengguna` dapat mencatat 0 atau banyak (`0..*`) `transaksi`.<br>• Satu `transaksi` dicatat oleh tepat 1 (`1..1`) `pengguna`. | **1 : N** | `pengguna_id` pada tabel `transaksi` |
| **2** | **`kategori`** — mengelompokkan — **`menu`** | • Satu `kategori` dapat mengelompokkan 1 atau banyak (`1..*`) `menu`.<br>• Satu `menu` termasuk ke dalam tepat 1 (`1..1`) `kategori`. | **1 : N** | `kategori_id` pada tabel `menu` |
| **3** | **`transaksi`** — memuat — **`detail_transaksi`** | • Satu `transaksi` memuat 1 atau banyak (`1..*`) `detail_transaksi`.<br>• Satu `detail_transaksi` dimiliki oleh tepat 1 (`1..1`) `transaksi`. | **1 : N** | `transaksi_id` pada tabel `detail_transaksi` |
| **4** | **`menu`** — terjual_dalam — **`detail_transaksi`** | • Satu `menu` dapat terjual dalam 0 atau banyak (`0..*`) `detail_transaksi`.<br>• Satu `detail_transaksi` merujuk ke tepat 1 (`1..1`) `menu`. | **1 : N** | `menu_id` pada tabel `detail_transaksi` |

---

## 2. Resolusi Relasi Banyak-ke-Banyak (*Many-to-Many Resolution*)

### Masalah Awal:
Relasi konseptual antara entitas `transaksi` dan entitas `menu` adalah **Banyak-ke-Banyak ($N:M$)**:
- Satu nota `transaksi` dapat membeli banyak item `menu` (misal: Nasi Rawon, Ayam Goreng, Es Teh).
- Satu item `menu` (misal: Es Teh) dapat dibeli dalam banyak nota `transaksi` oleh pelanggan berbeda.

### Solusi Pemecahan:
Sesuai aturan baku perancangan basis data relasional (Jobsheet 6 Bagian 2.1 & Langkah 4):
1. Relasi $N:M$ dipecah menjadi dua relasi satu-ke-banyak ($1:N$) dengan menambahkan tabel penghubung (*junction table*): **`detail_transaksi`**.
2. Atribut relasi dipindahkan ke tabel penghubung:
   - `jumlah` (kuantitas porsi pesanan).
   - `harga_satuan` (harga jual per porsi saat transaksi berlangsung).
   - `catatan` (keterangan khusus untuk dapur/bar).
3. **Hasil:** Tidak ada relasi $N:M$ yang tersisa tanpa tabel penghubung. Seluruh data transaksi dapat dinormalisasi dengan benar tanpa redundansi.

---

## 3. Notasi Kardinalitas Mermaid (Persiapan ERD Langkah 5)

Berikut adalah pemetaan simbol notasi *crow's foot* yang akan digunakan pada `erd.mmd`:
- `pengguna ||--o{ transaksi : mencatat` (Tepat satu pengguna $\rightarrow$ nol atau banyak transaksi)
- `kategori ||--|{ menu : mengelompokkan` (Tepat satu kategori $\rightarrow$ satu atau banyak menu)
- `transaksi ||--|{ detail_transaksi : memuat` (Tepat satu transaksi $\rightarrow$ satu atau banyak detail transaksi)
- `menu ||--o{ detail_transaksi : terjual_dalam` (Tepat satu menu $\rightarrow$ nol atau banyak detail transaksi)
