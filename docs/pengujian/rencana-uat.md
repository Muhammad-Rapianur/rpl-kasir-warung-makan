# Rencana User Acceptance Testing (UAT) — KasirWarung
**Proyek:** Sistem Informasi Kasir Warung Makan (`rpl-kasir-warung-makan`)  
**Penyusun:** Muhammad Rapianur (NIM: 24554010004)  
**Mata Kuliah:** Rekayasa Perangkat Lunak — Praktikum 13 (Tugas Lab 12)  
**Tanggal Penyusunan:** 20 November 2026  
**Target Pelaksanaan:** Minggu 14 (Pertemuan 14)  

---

## 1. Informasi Umum Pengujian Penerimaan

* **Tujuan:**  
  Memastikan pemilik warung makan dan kasir dapat menggunakan aplikasi KasirWarung secara lancar untuk pekerjaan operasional harian: mencatat pesanan makanan/minuman pembeli, menghitung otomatis uang kembalian tunai, mengelola daftar hidangan, serta melihat riwayat penjualan harian tanpa kendala teknis.
* **Peserta Pengujian:**  
  * **Pihak Klien / Pengguna:**
    1. **Pak Joko** — Pemilik Warung Makan (Peran: `pemilik`)
    2. **Siti Rahma** — Petugas Kasir Warung (Peran: `kasir`)
  * **Pengamat / Fasilitator:**
    * **Muhammad Rapianur** (Pengembang Sistem / Mahasiswa D3 TI Politeknik Sampit)
* **Jadwal & Tempat:**  
  * **Hari/Tanggal:** Jumat, 27 November 2026 (Minggu 14)
  * **Waktu:** 14:00 – 15:30 WIB (Durasi: 90 menit)
  * **Tempat:** Warung Makan Mitra, Jl. Tjilik Riwut, Sampit
* **Lingkungan & Data Uji:**  
  * Aplikasi dijalankan pada laptop pengembang (lingkungan uji lokal web server).
  * Menggunakan basis data terisolasi berisi **data hidangan karangan** (Menu: Ayam Bakar, Nasi Goreng, Es Teh Manis, Soto Ayam, dll.).
  * **Etika & Keamanan:** Tidak menggunakan data pribadi pelanggan nyata warung.
  * Akun pengujian yang disiapkan: `pak_joko` (pemilik) dan `siti_kasir` (kasir).
* **Kriteria Kelulusan (Acceptance Criteria):**  
  1. Seluruh skenario inti UAT (UAT-1 s.d. UAT-6) berstatus **Lulus**.
  2. Tidak ada cacat tingkat **Kritis** atau **Tinggi** yang ditemukan selama pengujian.
  3. Klien (Pemilik & Kasir) menyatakan bahwa aplikasi mudah dipahami dan siap menggantikan nota kertas manual.
* **Cara Merekam Temuan:**  
  Fasilitator mengamati dan mencatat setiap interaksi, komentar, atau kebingungan pengguna pada tabel lembar kerja skenario di bawah. Temuan yang berupa kegagalan sistem dipindahkan ke `docs/pengujian/laporan-cacat.md`.

---

## 2. Matriks Skenario UAT (Bahasa Operasional Kasir Warung Makan)

| ID | Kebutuhan (KF) | Skenario Alur Kerja (Bahasa Klien Warung) | Langkah Pengujian | Hasil yang Diharapkan Pengguna | Hasil Aktual | Status | Catatan Pengguna |
|:---:|:---:|:---|:---|:---|:---:|:---:|:---|
| **UAT-1** | KF-01, KF-02 | **Menambah hidangan masakan baru yang mulai dijual hari ini** | 1. Masuk sebagai Pemilik (`pak_joko`).<br>2. Buka menu **Katalog Menu** $\rightarrow$ klik tombol **Tambah Menu**.<br>3. Ketik nama `"Ayam Penyet Sambal Ijo"`.<br>4. Pilih kategori *"Makanan Utama"*.<br>5. Masukkan harga jual `22000`.<br>6. Pilih status *"Tersedia"* $\rightarrow$ klik **Simpan Menu**. | Menu hidangan baru langsung muncul pada daftar katalog menu dan dapat dipilih oleh kasir saat melayani pembeli. | — | Belum Dijalankan | Diuji pada pertemuan 14 |
| **UAT-2** | KF-04, KF-06, KF-09 | **Melayani pembeli makan di tempat (Dine-in) dengan pembayaran tunai** | 1. Masuk sebagai Kasir (`siti_kasir`).<br>2. Buka **+ Transaksi Baru**.<br>3. Pilih hidangan *"Nasi Goreng Spesial"*.<br>4. Masukkan jumlah porsi `2`.<br>5. Pilih tipe pesanan *"Makan di Tempat"* dan isi Meja `04`.<br>6. Masukkan uang tunai yang diserahkan pembeli `50000` (total tagihan Rp 40.000).<br>7. Klik **Simpan Transaksi**. | Sistem menyimpan pesanan, menerbitkan nomor nota kasir (`TRX-YYYYMMDD-XXX`), dan menampilkan uang kembalian pembeli pas sebesar **Rp 10.000**. | — | Belum Dijalankan | Diuji pada pertemuan 14 |
| **UAT-3** | KF-07 | **Kasir diingatkan sistem ketika uang pembayaran tunai pembeli kurang** | 1. Masuk sebagai Kasir.<br>2. Masukkan pesanan makanan dengan total belanja Rp 35.000.<br>3. Kasir salah mengetik uang yang diterima menjadi `20000`.<br>4. Klik tombol **Simpan Transaksi**. | Sistem menolak menyimpan transaksi dan memunculkan pesan peringatan jelas bahwa uang pembayaran tunai masih kurang. | — | Belum Dijalankan | Diuji pada pertemuan 14 |
| **UAT-4** | KF-02, KF-05 | **Mengubah status menu masakan yang sudah habis di etalase warung** | 1. Masuk sebagai Pemilik.<br>2. Buka **Katalog Menu** $\rightarrow$ cari hidangan *"Rendang Sapi"*.<br>3. Klik tombol **Ubah**.<br>4. Ubah pilihan status menjadi *"Habis"*.<br>5. Klik tombol **Simpan**. | Status hidangan pada katalog berubah menjadi tanda merah *"Habis"*, sehingga kasir mengetahui hidangan tersebut tidak dapat dipesan lagi. | — | Belum Dijalankan | Diuji pada pertemuan 14 |
| **UAT-5** | KF-Keamanan | **Petugas kasir tidak sengaja membuka halaman kelola harga pemilik** | 1. Masuk sebagai Kasir.<br>2. Periksa bahwa pada layar kasir tidak terdapat tombol Tambah atau Ubah Harga Menu.<br>3. Kasir mencoba mengetik alamat `/menu/tambah` langsung pada peramban. | Sistem langsung memblokir akses dan memunculkan halaman ramah *"Akses Ditolak (403)"* yang menerangkan bahwa fitur ini hanya untuk Pemilik warung. | — | Belum Dijalankan | Diuji pada pertemuan 14 |
| **UAT-6** | KF-01, KF-11 | **Mengecek seluruh riwayat pesanan penjualan warung hari ini** | 1. Masuk sebagai Kasir atau Pemilik.<br>2. Buka menu **Riwayat Transaksi**.<br>3. Periksa daftar nota penjualan yang tampil. | Menampilkan seluruh transaksi penjualan berurutan lengkap dengan jam, nomor meja/bungkus, nama kasir yang melayani, rincian menu pesanan, dan total uang masuk. | — | Belum Dijalankan | Diuji pada pertemuan 14 |

---

## 3. Format Persetujuan & Konfirmasi Jadwal Klien (Langkah 15)

### Catatan Konfirmasi Tertulis dari Klien:
> *“Skenario pengujian kasir (UAT-1 s.d. UAT-6) sudah kami pelajari bersama dan alurnya sangat cocok dengan operasional warung kami sehari-hari. Kami menyetujui jadwal pelaksanaan pada hari Jumat, 27 November 2026 jam 14.00 WIB di Warung Makan Mitra setelah jam istirahat makan siang selesai.”*  
> — **Pak Joko (Pemilik Warung Makan Mitra)**, dikonfirmasi via pesan tertulis pada 20 November 2026.

| Peran | Nama Terang | Status Persetujuan | Tanggal |
|:---|:---|:---:|:---:|
| **Pemilik Warung Makan** | Pak Joko | Disetujui (Konfirmasi Tertulis) | 20 November 2026 |
| **Petugas Kasir** | Siti Rahma | Disetujui (Konfirmasi Tertulis) | 20 November 2026 |
| **Pengembang Sistem** | Muhammad Rapianur | Diverifikasi & Siap UAT | 20 November 2026 |
