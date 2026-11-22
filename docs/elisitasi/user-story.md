# Daftar User Story & Kriteria Penerimaan (KasirWarung)

> **Mata Kuliah:** Rekayasa Perangkat Lunak (RPL) &mdash; D3 Teknologi Informasi, Politeknik Sampit  
> **Proyek:** Sistem Informasi Kasir &amp; Manajemen Transaksi Warung Makan (*KasirWarung*)  
> **Penyusun:** Muhammad Rapianur (NIM: 24554010004)  
> **Standar Penulisan:** INVEST Principle &amp; BDD (*Given-When-Then*)

---

## 📌 Ringkasan Pemetaan Epik &amp; Kebutuhan

| Kode Epik | Nama Epik Fitur | User Story Terkait | Pemetaan Kebutuhan (SRS / PRD) |
|---|---|---|---|
| **EP-01** | Autentikasi &amp; Kontrol Akses Peran | US-01, US-02, US-03 | KF-07, KF-08, KNF-06 (UC-01) |
| **EP-02** | Pengelolaan Menu &amp; Kategori Hidangan | US-04, US-05, US-06, US-07 | KF-01, KF-02, KF-05, KF-06 (UC-02, UC-03) |
| **EP-03** | Pencatatan Transaksi Penjualan (POS) | US-08, US-09, US-10 | KF-03, KF-04, KF-09, KF-10 (UC-04, UC-05) |
| **EP-04** | Riwayat Transaksi &amp; Rekapitulasi Omzet | US-11, US-12 | KF-11, KF-12, KF-13 (UC-06, UC-07) |
| **EP-05** | Keamanan Sistem &amp; Pencadangan Data | US-13, US-14 | KNF-01 s.d. KNF-06 |

---

## 1. Epik 1: Autentikasi &amp; Kontrol Akses Peran

### US-01: Masuk ke Sistem (Login)
* **Pernyataan User Story:**  
  *Sebagai* **Kasir atau Pemilik Warung**,  
  *saya ingin* **masuk ke dalam aplikasi menggunakan nama pengguna dan kata sandi yang sah**,  
  *agar* **hanya staf warung yang berhak yang dapat mengakses data transaksi dan katalog hidangan**.
* **Kriteria INVEST:**  
  *Independent* (mandiri), *Negotiable* (panjang sandi &ge;8 karakter), *Valuable* (mencegah akses liar), *Estimable* (3 SP), *Small* (1 siklus kerja), *Testable* (teruji status 200 vs 401).
* **Kriteria Penerimaan (*Given-When-Then*):**
  * **Skenario 1.1 (Login Sukses):**  
    *Given* pengguna berada di halaman `/login` dan memiliki akun terdaftar (contoh: `siti_kasir` / `siti12345`),  
    *When* pengguna memasukkan username dan kata sandi yang benar lalu menekan tombol "Masuk",  
    *Then* sistem membuat sesi terenkripsi, menampilkan pesan selamat datang, dan mengarahkan pengguna ke halaman `/menu`.
  * **Skenario 1.2 (Kredensial Salah):**  
    *Given* pengguna berada di halaman `/login`,  
    *When* pengguna memasukkan kata sandi yang salah,  
    *Then* sistem menolak autentikasi, mengembalikan status HTTP 401, dan menampilkan pesan umum *"Nama pengguna atau kata sandi salah"*.

### US-02: Keluar dari Sistem (Logout Aman)
* **Pernyataan User Story:**  
  *Sebagai* **Pengguna Aktif (Kasir/Pemilik)**,  
  *saya ingin* **keluar dari sesi aplikasi melalui metode POST**,  
  *agar* **sesi kerja saya berakhir dan tidak dapat disalahgunakan oleh orang lain setelah pergantian shift**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* pengguna sedang dalam keadaan terautentikasi (login aktif),  
  * *When* pengguna menekan tombol "Keluar" (mengirimkan form POST ber-CSRF token ke `/logout`),  
  * *Then* sistem menghapus seluruh data sesi di server dan mengalihkan layar kembali ke halaman `/login`.

### US-03: Pembatasan Hak Akses Kasir (RBAC)
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **sistem menolak akses kasir ke halaman penambahan menu, edit harga, dan kelola kategori**,  
  *agar* **kasir tidak dapat mengubah data master harga atau menghapus data penting warung makan**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* kasir (`siti_kasir`) sedang masuk ke dalam sistem,  
  * *When* kasir mencoba membuka tautan manajerial secara langsung di browser (contoh: `GET /menu/tambah` atau `GET /kategori`),  
  * *Then* server menolak permintaan dengan status **HTTP 403 Forbidden** dan menampilkan halaman antarmuka ramah *"403 — Akses Ditolak"*.

---

## 2. Epik 2: Pengelolaan Menu &amp; Kategori Hidangan

### US-04: Menampilkan &amp; Mencari Katalog Menu
* **Pernyataan User Story:**  
  *Sebagai* **Kasir**,  
  *saya ingin* **melihat daftar seluruh menu hidangan dan mencari berdasarkan nama makanan**,  
  *agar* **saya dapat memeriksa harga dan ketersediaan menu yang dipesan pelanggan secara cepat**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* pengguna berada di halaman `/menu`,  
  * *When* pengguna mengetik kata kunci *"Ayam"* pada kotak pencarian dan menekan "Cari",  
  * *Then* sistem menampilkan seluruh hidangan yang memuat kata *"Ayam"* (contoh: *Ayam Bakar, Ayam Goreng*) secara aman tanpa kerentanan SQL Injection.

### US-05: Menambah Menu Hidangan Baru (Khusus Pemilik)
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **menambahkan hidangan makanan/minuman baru beserta kategori dan harga jualnya**,  
  *agar* **katalog warung makan selalu mutakhir saat ada variasi menu baru**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* pemilik login dan membuka form `/menu/tambah`,  
  * *When* pemilik mengisi nama *"Bebek Bakar"*, kategori *"Sayur &amp; Lauk Pauk"*, dan harga `25000` lalu menekan "Simpan Menu",  
  * *Then* sistem menyimpan menu ke database dan menampilkan notifikasi sukses di daftar menu.
  * *When* pemilik menginput harga bernilai minus (`-5000`) atau huruf (`dua puluh ribu`),  
  * *Then* sistem menolak input di lapis server dan memunculkan pesan galat *"Harga harus berupa bilangan bulat positif"*.

### US-06: Mengubah Data Menu &amp; Status Ketersediaan
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **mengubah harga hidangan dan menandai status menu menjadi 'habis'**,  
  *agar* **harga jual selalu sinkron dengan modal bahan dan kasir mengetahui lauk yang sudah habis di dapur**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* menu *Ikan Goreng* berstatus 'tersedia',  
  * *When* pemilik membuka form ubah menu, mengganti status menjadi 'habis', dan menekan "Perbarui",  
  * *Then* status hidangan berubah menjadi 'habis' di katalog dan kasir tidak dapat memilih menu tersebut untuk transaksi baru.

### US-07: Mengelola Kategori Hidangan
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **menambah, mengubah, dan menghapus kategori kelompok menu**,  
  *agar* **hidangan warung makan dapat dikelompokkan dengan rapi (Makanan Utama, Minuman, Sayuran, Lauk)**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* kategori *"Sayuran"* masih memiliki relasi hidangan aktif di tabel menu,  
  * *When* pemilik mencoba menghapus kategori tersebut,  
  * *Then* sistem menolak penghapusan dengan aturan RESTRICT kunci asing dan memberi pesan bahwa kategori masih digunakan oleh menu hidangan.

---

## 3. Epik 3: Pencatatan Transaksi Penjualan Kasir (POS)

### US-08: Mencatat Transaksi Penjualan Multi-Item
* **Pernyataan User Story:**  
  *Sebagai* **Kasir**,  
  *saya ingin* **memilih beberapa menu makanan/minuman sekaligus dan memasukkan jumlah porsi pesanan**,  
  *agar* **pesanan meja pelanggan dapat dicatat lengkap dalam satu struk transaksi**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* kasir membuka form `/transaksi/tambah`,  
  * *When* kasir memilih menu *Ayam Bakar* (2 porsi @Rp 18.000) dan *Es Teh Manis* (2 porsi @Rp 5.000),  
  * *Then* sistem secara otomatis menghitung subtotal pesanan (Rp 36.000 dan Rp 10.000) dan total transaksi sebesar Rp 46.000 secara matematis tanpa kesalahan.

### US-09: Validasi Masukan Porsi &amp; Anti Overflow
* **Pernyataan User Story:**  
  *Sebagai* **Sistem**,  
  *saya ingin* **memvalidasi jumlah porsi hanya angka bulat positif dan menolak angka ekstrem atau karakter Unicode**,  
  *agar* **perhitungan transaksi stabil dan terhindar dari galat crash 500 (Cacat D-01 &amp; D-02)**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* kasir mengisi porsi kuantitas pada form transaksi,  
  * *When* kuantitas diisi angka `0`, minus `-2`, karakter pangkat dua `²`, atau angka lebih dari 1 miliar,  
  * *Then* sistem menolak transaksi dan menampilkan pesan galat spesifik tanpa merusak integritas basis data.

### US-10: Penyimpanan Transaksi Atomik (Database Transaction)
* **Pernyataan User Story:**  
  *Sebagai* **Sistem Database**,  
  *saya ingin* **menyimpan data nota ke tabel transaksi dan detail transaksi dalam satu transaksi atomik (COMMIT / ROLLBACK)**,  
  *agar* **tidak pernah terjadi nota transaksi tersimpan tanpa detail belanjaan saat terjadi kegagalan jaringan/listrik**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* proses penyimpanan transaksi sedang berjalan,  
  * *When* terjadi galat integritas pada baris detail transaksi kedua,  
  * *Then* sistem membatalkan seluruh operasi (*rollback* otomatis) sehingga basis data tetap bersih dan konsisten.

---

## 4. Epik 4: Riwayat Transaksi &amp; Rekapitulasi Omzet

### US-11: Melihat Riwayat Transaksi Penjualan
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik dan Kasir**,  
  *saya ingin* **melihat daftar riwayat transaksi yang diurutkan dari yang terbaru**,  
  *agar* **kasir dapat memeriksa pesanan yang baru diselesaikan dan pemilik dapat meninjau arus pesanan**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* pengguna membuka halaman `/transaksi`,  
  * *Then* sistem menyajikan tabel daftar transaksi memuat nomor transaksi (`TRX-`), tanggal, nama kasir pelayan, rincian menu yang dibeli, dan total rupiah belanja.

### US-12: Rekapitulasi Pendapatan Harian
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **melihat akumulasi total omzet harian saat penutupan warung makan**,  
  *agar* **saya dapat mencocokkan uang fisik di laci kasir dalam 1 menit tanpa perlu menghitung kertas bon manual**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* pemilik membuka laporan riwayat transaksi hari ini,  
  * *Then* sistem menampilkan agregasi jumlah total penjualan hari ini dan total transaksi yang berhasil diproses.

---

## 5. Epik 5: Keamanan Sistem &amp; Pencadangan Data

### US-13: Proteksi Serangan Brute-Force (Rate Limiter 429)
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Sistem**,  
  *saya ingin* **sistem memblokir sementara percobaan masuk jika terjadi kegagalan kata sandi lebih dari 5 kali**,  
  *agar* **akun kasir dan pemilik terlindungi dari upaya peretasan tebak kata sandi (*dictionary attack*)**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* seseorang mencoba masuk di form `/login`,  
  * *When* terjadi 5 kali kegagalan login berturut-turut dalam kurun waktu 5 menit,  
  * *Then* pada percobaan ke-6 server menolak request dengan status **HTTP 429 Too Many Requests** dan akun dikunci sementara selama 5 menit.

### US-14: Pencadangan Basis Data Mandiri (*Online Backup*)
* **Pernyataan User Story:**  
  *Sebagai* **Pemilik Warung**,  
  *saya ingin* **mencadangkan file basis data secara berkala tanpa mematikan aplikasi kasir yang sedang berjalan**,  
  *agar* **riwayat penjualan warung aman dari kerusakan komputer atau kehilangan data**.
* **Kriteria Penerimaan (*Given-When-Then*):**
  * *Given* aplikasi kasir sedang melayani pesanan pembeli,  
  * *When* perintah `python cadangkan.py` dieksekusi,  
  * *Then* sistem memanfaatkan SQLite Backup API untuk menyalin basis data ke folder `cadangan/kasir-YYYYMMDD-HHMMSS.db` secara utuh dan aman.
