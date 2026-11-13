# Verifikasi dan Pengujian Draf Skema AI — KasirWarung
## Langkah 9 & 10 Sesi 2: Jobsheet 6 Praktikum RPL

Dokumen ini memuat catatan pelaksanaan **Langkah 9 (Draf DDL AI & Asumsi)** dan **Langkah 10 (Verifikasi Daftar Periksa Lampiran E & Eksekusi Skrip Uji)** untuk proyek **Sistem Kasir Warung Makan (*KasirWarung*)**.

---

## Bagian 1: Pelaksanaan Langkah 9 (Draf DDL dari AI & Daftar Asumsi)

### 1.1 Prompt yang Digunakan
```text
Konteks: Berikut kamus data dan ERD (Mermaid) proyek KasirWarung. aturan-proyek.md: tech stack SQLite, Python 3.10+, Flask.
Tujuan: Buat skema SQLite (CREATE TABLE) untuk semua tabel (pengguna, kategori, menu, transaksi, detail_transaksi).
Batasan: Hanya tabel dan kolom yang ada pada kamus data; jangan menambah kolom turunan; uang bertipe INTEGER; tanggal TEXT format ISO; sertakan PRIMARY KEY, NOT NULL, UNIQUE, CHECK, dan REFERENCES; awali dengan PRAGMA foreign_keys = ON.
Format keluaran: Satu blok kode SQL, lalu daftar singkat asumsi yang kamu buat.
```

### 1.2 Draf Kode SQL DDL
Kode tersimpan di berkas [`docs/desain/schema.sql`](schema.sql).

### 1.3 Daftar Asumsi yang Dibuat AI
1. **Asumsi 1:** Warung makan hanya mengenal dua peran pengguna, yaitu `'kasir'` dan `'pemilik'`, sehingga dibatasi dengan `CHECK (peran IN ('kasir', 'pemilik'))`.
2. **Asumsi 2:** Warung makan tidak mengelola stok kuantitas angka (karena masakan segar harian), melainkan status ketersediaan menu `'tersedia'` atau `'habis'`.
3. **Asumsi 3:** Kolom `total_bayar` dan `kembalian` tidak disimpan di tabel `transaksi` karena merupakan nilai turunan matematis yang dihitung saat kueri (`SUM`).
4. **Asumsi 4:** Pesanan *Bungkus (take_away)* tidak membutuhkan nomor meja, sehingga `nomor_meja` diizinkan bernilai `NULL`.
5. **Asumsi 5:** Penghapusan data transaksi induk akan secara otomatis menghapus rincian item pesanan terkait menggunakan aturan `ON DELETE CASCADE`.

---

## Bagian 2: Pelaksanaan Langkah 10 (Verifikasi dengan Daftar Periksa Lampiran E)

### 2.1 Tabel Daftar Periksa Verifikasi Skema (Lampiran E.1)

| No | Pertanyaan Periksa | Hasil | Catatan Pemeriksaan |
| :-: | :--- | :---: | :--- |
| 1 | Semua tabel dan kolom ada di kamus data/ERD? Adakah kolom tambahan liar dari AI? | **Ya** | Tepat 5 tabel (`pengguna`, `kategori`, `menu`, `transaksi`, `detail_transaksi`). Tidak ada tabel liar. |
| 2 | Kardinalitas pada ERD benar jika dibaca dari dua arah? | **Ya** | Seluruh relasi $1:N$ konsisten dengan kalimat dua arah pada Langkah 4. |
| 3 | Relasi banyak-ke-banyak sudah dipecah dengan tabel penghubung? | **Ya** | Relasi `transaksi` $\leftrightarrow$ `menu` dipecah oleh `detail_transaksi`. |
| 4 | Tidak ada kolom turunan (misal total tagihan) atau data ganda? | **Ya** | `total_bayar` dan `kembalian` tidak dibuatkan kolom fisik. |
| 5 | Setiap tabel punya PK; setiap FK mengacu tabel yang benar? | **Ya** | Seluruh tabel memiliki `id INTEGER PRIMARY KEY AUTOINCREMENT` dan FK merujuk ke tabel induk yang sah. |
| 6 | Batasan NOT NULL, UNIQUE, dan CHECK sesuai aturan? | **Ya** | Batasan harga $\ge 0$, kuantitas $> 0$, uang diterima $\ge 0$, status valid, dan peran valid aktif. |
| 7 | Uang bertipe INTEGER, tanggal TEXT ISO, kata sandi berupa hash? | **Ya** | Uang tanpa desimal (`INTEGER`), tanggal ISO (`TEXT`), kata sandi `password_hash`. |
| 8 | Perintah `PRAGMA foreign_keys = ON;` ada di baris pertama? | **Ya** | Dinyatakan eksplisit di awal berkas `schema.sql`. |
| 9 | Skrip uji: semua perintah pelanggaran ditolak? | **Ya** | Terbukti lolos 13 skenario uji pada `tests/cek_skema.py`. |
| 10 | Struktur folder dan lapisan sesuai `aturan-proyek.md`? | **Ya** | Skema di `docs/desain/schema.sql` dan skrip uji di `tests/cek_skema.py`. |

---

### 2.2 Tabel Temuan Verifikasi Draf AI (Format Langkah 10)

| No | Temuan pada Draf AI | Tabel / Kolom | Valid? | Tindakan Perbaikan |
| :-: | :--- | :--- | :---: | :--- |
| **1** | Kecenderungan AI umum menambahkan kolom `total_bayar` dan `kembalian` pada tabel transaksi. | `transaksi` | **Tidak Valid (Melanggar aturan)** | Kolom `total_bayar` dan `kembalian` dihapus dari tabel `transaksi`. Nilai dihitung dinamis menggunakan kueri `SUM(jumlah * harga_satuan)`. |
| **2** | Perintah `PRAGMA foreign_keys = ON;` sering lupa disertakan oleh AI jika tidak diminta eksplisit. | Root skrip SQL | **Valid (Harus Ada)** | Menambahkan `PRAGMA foreign_keys = ON;` pada baris pertama `schema.sql` agar penegakan FK aktif di SQLite. |
| **3** | Batasan kuantitas pemesanan menu belum mencegah angka 0 atau negatif jika hanya mengandalkan tipe data integer. | `detail_transaksi.jumlah` | **Valid (Harus Diperbaiki)** | Menambahkan batasan `CHECK (jumlah > 0)` agar pesanan menu bernilai minimal 1 porsi. |
| **4** | Nilai default status ketersediaan menu belum didefinisikan secara otomatis. | `menu.status` | **Valid (Harus Diperbaiki)** | Menambahkan klausa `DEFAULT 'tersedia'` dan batasan `CHECK (status IN ('tersedia', 'habis'))`. |
| **5** | Integritas data saat transaksi dihapus berisiko menyisakan data yatim (*orphan records*) pada rincian pesanan. | `detail_transaksi.transaksi_id` | **Valid (Harus Diperbaiki)** | Menambahkan klausa `ON DELETE CASCADE` pada foreign key `transaksi_id`. |

---

### 2.3 Kesalahan AI yang Paling Berisiko Bagi Data Klien
> **Kesalahan Paling Berisiko:**  
> **Lupa mengaktifkan `PRAGMA foreign_keys = ON;` dan menyimpan data turunan `total_bayar` secara redundan.**
>
> *Alasan Risiko:*  
> Secara bawaan (*default*), mesin SQLite **mengabaikan integritas kunci asing (*foreign keys*)** jika pragma ini tidak dieksekusi pada setiap sesi koneksi. Tanpa pragma ini, sistem kasir dapat memasukkan `detail_transaksi` dengan ID transaksi atau ID menu fiktif tanpa memicu error, yang berakibat pada kekacauan pembukuan laporan kas warung. Selain itu, menyimpan `total_bayar` berisiko menimbulkan selisih kas (*data discrepancy*) jika rincian menu di nota diubah tetapi totalnya lupa diperbarui.

---

## Bagian 3: Bukti Eksekusi Skrip Uji (`tests/cek_skema.py`)

Perintah yang dijalankan dari terminal utama proyek:
```bash
python tests/cek_skema.py
```

### Keluaran Terminal (Output Pengujian):
```text
=======================================================
  Pengujian Integritas Skema — KasirWarung
=======================================================

[1] Uji Struktur Tabel & Seed Data
  [LULUS] Semua 5 tabel wajib ada di skema
  [LULUS] Seed data kategori minimal 4 baris
  [LULUS] Seed data menu minimal 1 baris

[2] Uji Batasan Data (CHECK Constraints)
  [LULUS] Tolak harga menu bernilai negatif
  [LULUS] Tolak status menu di luar 'tersedia/habis'
  [LULUS] Tolak peran pengguna di luar kasir/pemilik
  [LULUS] Tolak metode bayar di luar tunai/qris
  [LULUS] Tolak tipe pesanan di luar dine_in/take_away
  [LULUS] Tolak jumlah item detail = 0 atau negatif

[3] Uji Integritas Referensial (Foreign Keys)
  [LULUS] Tolak menu dengan kategori_id tidak ada
  [LULUS] Tolak transaksi dengan pengguna_id tidak ada
  [LULUS] Tolak username pengguna duplikat
  [LULUS] CASCADE DELETE: detail terhapus saat transaksi induk dihapus

=======================================================
  Hasil : 13 LULUS  |  0 GAGAL
=======================================================
  ✅ Semua pengujian lulus! Skema siap digunakan.
```
