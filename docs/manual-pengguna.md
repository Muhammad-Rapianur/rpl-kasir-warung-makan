# 📖 Buku Panduan Pengguna: Sistem KasirWarung

> **Aplikasi Kasir & Manajemen Warung Makan Sederhana**  
> Ditujukan untuk: **Pemilik Warung Makan** dan **Petugas Kasir**  
> Versi Aplikasi: **1.0.0**

Selamat datang di sistem **KasirWarung**. Buku panduan ini disusun langkah demi langkah untuk membantu Anda melayani pesanan pelanggan dan mengelola warung makan dengan cepat, mudah, dan akurat.

---

## 📑 Daftar Isi
1. [Cara Masuk ke Aplikasi (Login)](#1-cara-masuk-ke-aplikasi-login)
2. [Melihat dan Mencari Menu Hidangan](#2-melihat-dan-mencari-menu-hidangan)
3. [Mencatat Transaksi Penjualan Baru (Tugas Utama Kasir)](#3-mencatat-transaksi-penjualan-baru-tugas-utama-kasir)
4. [Melihat Riwayat Transaksi Penjualan](#4-melihat-riwayat-transaksi-penjualan)
5. [Menambah dan Mengubah Menu Hidangan (Khusus Pemilik)](#5-menambah-dan-mengubah-menu-hidangan-khusus-pemilik)
6. [Kelola Kategori Hidangan (Khusus Pemilik)](#6-kelola-kategori-hidangan-khusus-pemilik)
7. [Cara Keluar dari Sistem (Logout)](#7-cara-keluar-dari-sistem-logout)
8. [Tabel Bantuan: Bila Ada Masalah](#8-tabel-bantuan-bila-ada-masalah)

---

## 1. Cara Masuk ke Aplikasi (Login)

1. Buka peramban web (Google Chrome / Mozilla Firefox / Microsoft Edge) pada komputer warung.
2. Ketik alamat kasir: `http://localhost:5000` (atau alamat IP lokal yang diberikan teknisi, contoh: `http://192.168.1.5:8000`).
3. Anda akan melihat halaman masuk sistem:

```text
+-----------------------------------------------------------+
|                       KasirWarung                         |
|                                                           |
|                       MASUK SISTEM                        |
|        Aplikasi Kasir & Manajemen Warung Makan            |
|                                                           |
|   Nama Pengguna (Username):                               |
|   [ siti_kasir                                       ]    |
|                                                           |
|   Kata Sandi (Password):                                  |
|   [ **********                                       ]    |
|                                                           |
|   [               TOMBOL: MASUK                      ]    |
|                                                           |
|              KasirWarung v1.0.0                           |
+-----------------------------------------------------------+
```

4. Ketik **Nama Pengguna** dan **Kata Sandi** akun Anda.
5. Klik tombol biru **Masuk**.
6. Jika data benar, Anda akan disambut dengan pesan: *"Selamat datang, [Nama Anda]!"* dan langsung diarahkan ke halaman Katalog Menu.

> ⚠️ **Peringatan Keamanan:** Jika Anda salah memasukkan kata sandi sebanyak 5 kali berturut-turut, sistem akan mengunci proses masuk selama 5 menit demi mencegah pencurian akun.

---

## 2. Melihat dan Mencari Menu Hidangan

Menu **Katalog Menu** menampilkan seluruh hidangan makanan dan minuman yang tersedia di warung:

1. Di bilah navigasi atas, klik **Katalog Menu**.
2. **Mencari hidangan tertentu:** Ketik nama makanan di kolom **Cari nama menu** (contoh: *Ayam Bakar* atau *Es Teh*), lalu klik tombol **Cari**.
3. **Menyaring kategori:** Pilih kelompok menu pada menu drop-down (*Makanan Utama, Sayur & Lauk Pauk, Minuman, Ekstra*).
4. Untuk mengembalikan tampilan ke seluruh daftar hidangan, klik tautan biru **Atur Ulang**.

---

## 3. Mencatat Transaksi Penjualan Baru (Tugas Utama Kasir)

Saat pelanggan memesan dan membayar di meja kasir:

1. Klik tombol **+ Transaksi Baru** di bilah navigasi atas.
2. Anda akan disajikan formulir pencatatan penjualan:
   * **Pilih Menu:** Pilih nama hidangan yang dipesan pelanggan dari daftar menu.
   * **Jumlah Porsi:** Masukkan angka porsi (contoh: `2`).
   * **Harga Satuan & Subtotal:** Sistem secara otomatis menghitung harga sesuai tarif resmi.
   * **Tambah Baris Menu:** Klik tombol tambah baris jika pelanggan memesan lebih dari satu jenis makanan/minuman.
3. Periksa kembali total belanjaan pelanggan.
4. Klik tombol **Simpan Transaksi**.
5. Transaksi berhasil tersimpan dengan notifikasi hijau, dan struk penjualan siap dicatat.

---

## 4. Melihat Riwayat Transaksi Penjualan

Untuk memeriksa penjualan harian atau rekap penjualan per kasir:

1. Klik menu **Riwayat Transaksi** di navigasi atas.
2. Layar akan menampilkan tabel ringkasan:
   * **Nomor Transaksi** (contoh: `#TRX-20261120-001`)
   * **Waktu & Tanggal**
   * **Nama Kasir yang Melayani**
   * **Daftar Pesanan & Total Belanja (Rp)**
3. Anda dapat meninjau rincian lengkap setiap transaksi kapan saja.

---

## 5. Menambah dan Mengubah Menu Hidangan (Khusus Pemilik)

> 🔒 **Hak Akses:** Hanya akun dengan peran **Pemilik Warung** yang dapat mengakses menu ini. Jika kasir mencoba mengakses, layar akan memunculkan peringatan *403 — Akses Ditolak*.

### A. Menambah Menu Baru
1. Masuk sebagai akun Pemilik (contoh: `pak_joko`).
2. Masuk ke halaman **Katalog Menu**, lalu klik tombol biru **+ Tambah Menu Baru** di kiri atas.
3. Masukkan data:
   * **Nama Menu:** contoh *Bebek Goreng Sambal Korek*
   * **Kategori:** pilih *Sayur & Lauk Pauk*
   * **Harga (Rp):** ketik nominal angka saja (contoh: `25000`)
4. Klik **Simpan Menu**.

### B. Mengubah Menu atau Mengganti Status Ketersediaan
1. Pada tabel menu hidangan, cari baris menu yang ingin diubah.
2. Klik tombol tautan **Ubah** di kolom aksi sebelah kanan.
3. Perbarui harga atau ubah status menjadi **Habis** jika bahan makanan sedang kosong.
4. Klik **Perbarui Menu**.

---

## 6. Kelola Kategori Hidangan (Khusus Pemilik)

1. Di navigasi atas, klik **Kelola Kategori**.
2. Anda dapat menambah kategori baru (contoh: *Paket Hemat* atau *Aneka Jus*).
3. Untuk menghapus kategori, pastikan tidak ada hidangan yang masih menggunakan kategori tersebut.

---

## 7. Cara Keluar dari Sistem (Logout)

Bila pergantian giliran kerja (*shift*) kasir atau warung telah tutup:

1. Lihat di pojok kanan atas layar navigasi.
2. Klik tombol abu-abu **Keluar**.
3. Sistem akan mengakhiri sesi kerja dengan aman dan kembali ke halaman Masuk Sistem.

---

## 8. Tabel Bantuan: Bila Ada Masalah

| Masalah / Pesan Galat yang Muncul | Penyebab | Tindakan yang Harus Dilakukan |
|---|---|---|
| **"Nama pengguna atau kata sandi salah"** | Salah ketik huruf besar/kecil atau salah kata sandi. | Periksa tombol Caps Lock keyboard, ketik ulang kata sandi dengan teliti. |
| **"Terlalu banyak percobaan login gagal. Silakan coba kembali dalam 5 menit."** | Salah kata sandi lebih dari 5 kali (fitur pengaman anti-pembobolan aktif). | Tunggu 5 menit tanpa menekan tombol masuk, lalu coba login kembali dengan kata sandi yang benar. |
| **"403 — Akses Ditolak: Peran Anda saat ini tidak diizinkan..."** | Petugas kasir mencoba membuka fitur manajerial (tambah menu, ubah harga, atau kelola kategori). | Klik tombol *"Kembali ke Daftar Menu"*. Fitur tersebut sengaja dikunci hanya untuk Pemilik Warung. |
| **"Halaman tidak dapat diakses / Server Not Found"** | Komputer server utama kasir belum dinyalakan atau kabel jaringan terlepas. | Pastikan komputer server utama menyala, server kasir berjalan, dan kabel jaringan LAN/Wi-Fi tersambung. |
| **"Jumlah harus berupa bilangan bulat positif"** | Mengisi porsi dengan huruf, tanda minus (`-`), atau angka nol (`0`). | Masukkan angka porsi minimal 1 (contoh: 1, 2, 3). |
| **"Lupa Kata Sandi"** | Pengguna lupa password akun kasir. | Hubungi Pemilik Warung. Pemilik dapat membuatkan akun baru lewat teknisi menggunakan skrip `buat_pengguna.py`. |

---

*KasirWarung v1.0.0 — Dibuat oleh Muhammad Rapianur (NIM: 24554010004) untuk Praktikum RPL D3 TI Politeknik Sampit.*
