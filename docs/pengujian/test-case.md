# Dokumen Test Case & Matriks Keterlacakan — KasirWarung
**Proyek:** Sistem Informasi Kasir Warung Makan (`rpl-kasir-warung-makan`)  
**Penyusun:** Muhammad Rapianur (NIM: 24554010004)  
**Mata Kuliah:** Rekayasa Perangkat Lunak — Praktikum 13 (Tugas Lab 12)  
**Tanggal:** 20 November 2026  
**Status:** Draf Pengujian Sesi 1  

---

## 1. Matriks Keterlacakan Kebutuhan Fungsional (Langkah 3 / Lampiran B.1)

Matriks berikut menghubungkan Kebutuhan Fungsional (KF) dari dokumen SRS/PRD ke rancangan Test Case untuk memastikan tidak ada celah pengujian (*test gap*).

| ID KF | Kebutuhan Fungsional (SRS) | Kriteria Penerimaan (Acceptance Criteria) | Test Case Terkait |
|:---:|:---|:---|:---:|
| **KF-01** | Katalog & Kategori Menu | Menampilkan daftar makanan/minuman terfilter kategori; kategori baru dapat dibuat dan divalidasi. | TC-13, TC-14, TC-15 |
| **KF-02** | Pengelolaan Menu & Harga | Pemilik dapat menambah menu baru; harga wajib bilangan bulat positif (Rp 1 s.d. Rp 1.000.000.000); status stok (tersedia/habis). | TC-01, TC-02, TC-03, TC-04, TC-05, TC-06, TC-07, TC-08, TC-09, TC-10, TC-11, TC-12 |
| **KF-04** | Perhitungan Subtotal & Total | Sistem menghitung subtotal (porsi × harga satuan) dan akumulasi total belanja secara otomatis; porsi harus bilangan bulat $> 0$. | TC-16, TC-17, TC-18, TC-19 |
| **KF-06** | Perhitungan Uang Kembalian | Sistem menghitung nominal uang kembalian (Uang Bayar − Total Belanja) secara presisi pada pembayaran tunai. | TC-20 |
| **KF-07** | Validasi Pembayaran Tunai | Sistem wajib menolak simpan transaksi jika nominal uang bayar tunai kurang dari total belanja yang harus dibayar. | TC-21 |
| **KF-09** | Nomor Transaksi Unik | Sistem menghasilkan nomor nota unik dengan format `TRX-YYYYMMDD-XXX` untuk setiap transaksi yang berhasil disimpan. | TC-22 |
| **KF-Keamanan** | Autentikasi & Otorisasi Peran | Kasir hanya bisa transaksi & riwayat; pemilik bisa kelola menu & kategori; form POST wajib membawa token CSRF valid. | TC-23, TC-24, TC-25, TC-26, TC-27, TC-28 |

---

## 2. Analisis Partisi Ekuivalen (EP) & Nilai Batas (BVA) (Langkah 4)

Tiga isian utama dengan aturan bisnis ketat pada KasirWarung dianalisis batas nilainya:

### A. Isian Harga Menu Makanan/Minuman (KF-02)
* **Aturan Bisnis:** Bilangan bulat, nilai minimum Rp 1, nilai maksimum Rp 1.000.000.000 (1 Miliar Rupiah).
* **Partisi Ekuivalen (EP):**
  * Valid: $1 \le \text{harga} \le 1.000.000.000$
  * Negatif/Nol: $\le 0$
  * Bukan Angka / Format Salah: teks alfabet, desimal pecahan, karakter unicode non-ASCII
  * Terlalu Besar: $> 1.000.000.000$ (dan angka raksasa $\ge 30$ digit)
* **Nilai Batas (BVA):**
  * Batas Bawah: $-1$ (invalid), $0$ (invalid), $1$ (valid)
  * Batas Atas: $1.000.000.000$ (valid), $1.000.000.001$ (invalid)

### B. Isian Jumlah Porsi Pesanan (KF-04)
* **Aturan Bisnis:** Minimal 1 porsi, bilangan bulat positif, tidak boleh pecahan atau minus.
* **Partisi Ekuivalen (EP):**
  * Valid: $\ge 1$
  * Tidak Valid: $\le 0$, desimal, kosong, simbol/huruf
* **Nilai Batas (BVA):**
  * $-1$ (invalid), $0$ (invalid), $1$ (valid batas bawah), $2$ (valid)

### C. Isian Akun Pengguna (Username & Password)
* **Aturan Bisnis:** Username alfanumerik 3–30 karakter; Password minimal 8 karakter.
* **Nilai Batas (BVA):**
  * Username: 2 karakter (invalid), 3 karakter (valid batas bawah), 30 karakter (valid batas atas), 31 karakter (invalid).
  * Password: 7 karakter (invalid), 8 karakter (valid batas bawah).

---

## 3. Tabel Rancangan 28 Test Case Black-Box (Langkah 4 / Lampiran B.2)

> **Keterangan Teknik:**  
> * **BVA:** Boundary Value Analysis (Analisis Nilai Batas)  
> * **EP:** Equivalence Partitioning (Partisi Ekuivalen)  
> * **Pelanggaran:** Uji masukan salah, format jahat, atau akses terlarang  
> * **Normal:** Uji alur standar  

| ID TC | KF | Teknik | Prasyarat | Masukan / Langkah | Hasil Diharapkan (PRD/SRS) | Hasil Aktual | Status |
|:---:|:---:|:---:|:---|:---|:---|:---|:---:|
| **TC-01** | KF-02 | BVA | Login Pemilik | Tambah menu dengan `harga = "0"` | Ditolak validasi, muncul pesan error harga harus $> 0$ | Ditolak validasi, galat harga muncul | **Lulus** |
| **TC-02** | KF-02 | BVA | Login Pemilik | Tambah menu dengan `harga = "1"` | Diterima, menu tersimpan dengan harga Rp 1 | Diterima, data["harga"] == 1 | **Lulus** |
| **TC-03** | KF-02 | EP | Login Pemilik | Tambah menu dengan `harga = "25000"` (Ayam Bakar) | Diterima, menu tersimpan harga Rp 25.000 | Diterima, data["harga"] == 25000 | **Lulus** |
| **TC-04** | KF-02 | EP | Login Pemilik | Tambah menu dengan `harga = " 15000 "` (ada spasi luar) | Diterima, spasi dipangkas menjadi 15000 | Diterima, spasi dipangkas bersih | **Lulus** |
| **TC-05** | KF-02 | BVA | Login Pemilik | Tambah menu dengan `harga = "1000000000"` (1 Miliar) | Diterima batas atas sistem | Diterima, data["harga"] == 1000000000 | **Lulus** |
| **TC-06** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = "-1"` | Ditolak validasi harga | Ditolak validasi bilangan bulat positif | **Lulus** |
| **TC-07** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = "15000.50"` (pecahan) | Ditolak validasi bilangan bulat | Ditolak validasi | **Lulus** |
| **TC-08** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = "gratis"` (alfabet) | Ditolak validasi angka | Ditolak validasi | **Lulus** |
| **TC-09** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = ""` (kosong) | Ditolak validasi wajib isi | Ditolak validasi | **Lulus** |
| **TC-10** | KF-02 | BVA | Login Pemilik | Tambah menu dengan `harga = "1000000001"` (1 Miliar + 1) | Ditolak validasi melebihi batas atas | Lolos validasi (belum ada batas atas) | **Gagal (D-02)** |
| **TC-11** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = "9" * 30` (30 digit) | Ditolak validasi aman, bukan galat 500 | Lolos validasi (potensi OverflowError) | **Gagal (D-02)** |
| **TC-12** | KF-02 | Pelanggaran | Login Pemilik | Tambah menu dengan `harga = "²"` (angka unicode) | Ditolak validasi aman, bukan galat 500 | Ditolak oleh handler uji coba | **Lulus** |
| **TC-13** | KF-01 | Normal | Login Pemilik | Tambah kategori `nama = "Minuman Segar"` | Diterima, kategori tersimpan | Diterima, tersimpan di database | **Lulus** |
| **TC-14** | KF-01 | Pelanggaran | Login Pemilik | Tambah kategori `nama = "   "` (hanya spasi) | Ditolak validasi nama kosong | Ditolak validasi nama | **Lulus** |
| **TC-15** | KF-01 | Pelanggaran | Login Pemilik | Hapus kategori yang masih memiliki menu aktif | Ditolak, integritas kunci asing (RESTRICT) terjaga | Ditolak SQLite IntegrityError aman | **Lulus** |
| **TC-16** | KF-04 | BVA | Login Kasir | Pesan menu dengan `jumlah_porsi = "1"` | Diterima, subtotal dihitung benar | Diterima, data["jumlah"] == 1 | **Lulus** |
| **TC-17** | KF-04 | BVA | Login Kasir | Pesan menu dengan `jumlah_porsi = "0"` | Ditolak validasi (porsi minimal 1) | Ditolak validasi kuantitas | **Lulus** |
| **TC-18** | KF-04 | Pelanggaran | Login Kasir | Pesan menu dengan `jumlah_porsi = "-1"` | Ditolak validasi porsi | Ditolak validasi | **Lulus** |
| **TC-19** | KF-04 | Pelanggaran | Login Kasir | Pesan menu dengan `jumlah_porsi = "dua"` | Ditolak validasi porsi | Ditolak validasi | **Lulus** |
| **TC-20** | KF-06 | Normal | Login Kasir | Total Rp 30.000, bayar tunai Rp 50.000 | Transaksi disimpan, kembalian Rp 20.000 | Kembalian Rp 20.000 dihitung pas | **Lulus** |
| **TC-21** | KF-07 | Pelanggaran | Login Kasir | Total Rp 30.000, bayar tunai Rp 20.000 | Ditolak, pesan "Uang bayar kurang" | Ditolak, flash pesan muncul | **Lulus** |
| **TC-22** | KF-09 | Normal | Login Kasir | Simpan transaksi penjualan baru | Nomor transaksi berformat `TRX-YYYYMMDD-XXX` | Format TRX-YYYYMMDD-XXX terbit | **Lulus** |
| **TC-23** | Keamanan | Pelanggaran | Tamu | Akses rute pemilik `GET /menu/tambah` | Ditolak, diarahkan (302) ke `/login` | HTTP 302 Redirect login | **Lulus** |
| **TC-24** | Keamanan | Pelanggaran | Login Kasir | Akses rute pemilik `GET /menu/tambah` | Ditolak dengan halaman 403 Forbidden | HTTP 403 Forbidden | **Lulus** |
| **TC-25** | Keamanan | Pelanggaran | Login Kasir | Akses rute kategori `GET /kategori` | Ditolak dengan halaman 403 Forbidden | HTTP 403 Forbidden | **Lulus** |
| **TC-26** | Keamanan | Pelanggaran | Login Pemilik | POST tanpa token CSRF pada `/menu/tambah` | Ditolak dengan status HTTP 400 Bad Request | HTTP 400 Bad Request | **Lulus** |
| **TC-27** | Keamanan | BVA | CLI Admin | Buat pengguna username 2 huruf | Ditolak, username minimal 3 karakter | Ditolak pesan validasi | **Lulus** |
| **TC-28** | Keamanan | BVA | CLI Admin | Buat pengguna password 7 karakter | Ditolak, kata sandi minimal 8 karakter | Ditolak pesan validasi | **Lulus** |

---

## 4. Ringkasan Hasil Eksekusi Sesi 1
* **Total Test Case Dievaluasi:** 28 Kasus
* **Jumlah Lulus:** 26 Kasus (**92.8%**)
* **Jumlah Gagal (Calon Cacat Sesi 2):** 2 Kasus (TC-10 & TC-11) ditambah 2 kasus fungsi input (Unicode `"²"` pada porsi dan Tanggal `"20261120"`).

### Daftar Calon Cacat yang Ditemukan (Untuk Diperbaiki di Sesi 2):
1. **Calon D-01:** Karakter unicode `"²"` pada porsi pesanan menyebabkan `ValueError: invalid literal for int() with base 10: '²'`.
2. **Calon D-02:** Harga menu melebihi 1 Miliar dan 30 digit angka lolos validasi tanpa batas atas, berpotensi memicu `OverflowError` di SQLite.
3. **Calon D-03:** Masukan tanggal tanpa tanda hubung (`20261120`) diterima oleh `date.fromisoformat()`, padahal format resmi yang diwajibkan adalah `YYYY-MM-DD`.

---

## 4. Komposisi Rancangan Test Case
* **BVA (Boundary Value Analysis):** 9 test case (TC-01, TC-02, TC-05, TC-10, TC-16, TC-17, TC-27, TC-28, dll)
* **Pelanggaran (Negative Testing):** 14 test case (TC-06 s.d. TC-09, TC-11, TC-12, TC-14, TC-15, TC-18, TC-19, TC-21, TC-23 s.d. TC-26)
* **Normal / EP Valid:** 5 test case (TC-03, TC-04, TC-13, TC-20, TC-22)
* **Total:** **28 Test Case** (Melampaui syarat minimal $\ge 20$ butir pada Jobsheet 13).

