# Bahan Paparan Design Review (Langkah 10) — KasirWarung

**Kelompok:** Tim RPL D3 TI (Proyek KasirWarung)  
**Waktu Paparan:** ± 5 Menit (5 Poin Paparan Utama)  
**Tautan Repositori:** `d:\RPL\rpl-kasir-warung-makan`

---

## 1. Gambaran Proyek dan Klien
- **Nama Sistem:** Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*).
- **Profil Klien:** Warung makan tradisional skala UMKM (lauk pauk prasmanan / ramesan).
- **Masalah Utama Klien:**
  1. Kasir sering salah menghitung uang kembalian saat jam makan siang yang ramai karena mengandalkan kalkulator fisik manual.
  2. Nota kertas rentan tercecer/hilang, menyulitkan rekap omzet harian.
  3. Pemilik warung kesulitan memisahkan uang kas tunai fisik di laci dengan pemasukan non-tunai via transfer QRIS statis.
- **Solusi:** Sistem POS berbasis web lokal (*offline-first*), responsif, tombol besar, validasi otomatis harga/stok habis, kalkulasi kembalian akurat, serta rekapitulasi omzet harian instan.

---

## 2. Peta Navigasi Antarmuka
Sistem menerapkan hierarki navigasi berbasis peran (*Role-Based Access Control* / RBAC):
```
[wf-01: Login]
      │
      ├──> (Role: Kasir)  ──> [wf-02: POS Kasir] ──> [wf-03: Struk Nota]
      │                              │
      │                              └──> [wf-05: Riwayat Transaksi]
      │
      └──> (Role: Pemilik) ──> [wf-04: Kelola Menu & Kategori]
                                     │
                                     ├──> [wf-05: Riwayat Transaksi]
                                     └──> [wf-06: Laporan Rekap Omzet]
```
- **Karakteristik Alur:** Efisien dan minim friksi; kasir dapat menyelesaikan pemesanan hingga struk dalam $\le 2$ klik utama.

---

## 3. Dua Wireframe Utama dan Anotasi
1. **`wf-02 POS Kasir` (Halaman Transaksi Kasir):**
   - **Katalog Grid Menu (Anotasi 01–03):** Kartu menu berukuran $\ge 48\text{ px}$, teks kontras $\ge 16\text{ px}$, dilengkapi tab filter kategori (Makanan, Minuman, Sayur, Gorengan).
   - **Indikator Menu Habis (Anotasi 04):** Kartu menu berstatus habis otomatis berwarna abu-abu redup (*disabled*) dengan label badge merah *"HABIS"*; sistem menampilkan *banner toast error* jika diklik kasir.
   - **Keranjang & Kalkulator Pembayaran (Anotasi 05–08):** Pilihan tipe *Dine-in / Take-away*, ringkasan item, input uang tunai dengan hitung kembalian *real-time*, dan tombol eksekusi transaksi yang terkunci (*disabled*) jika uang bayar kurang.
2. **`wf-04 Kelola Menu` (Halaman Manajemen Pemilik):**
   - **Form Tambah/Edit Menu (Anotasi 01–03):** Input nama, kategori dropdown, dan harga jual dengan validasi angka positif ($>0$).
   - **Toggle Cepat Ketersediaan (Anotasi 04):** Tombol sakelar (*switch toggle*) instan di tabel menu untuk mengubah status *Tersedia $\leftrightarrow$ Habis* tanpa perlu masuk form edit.

---

## 4. Ringkasan Rencana Pengujian & Matriks Keterlacakan
- **Strategi Pengujian:** Menggunakan 3 tingkatan: Black-Box Manual (peramban), Unit Test Otomatis (Python `unittest`), dan User Acceptance Test (UAT) bersama kasir warung.
- **Daftar Test Case:** 17 kasus uji (`TC-01` s.d. `TC-17`) yang mencakup:
  - 10 kebutuhan *Must Have* dan 3 kebutuhan *Should Have* (Cakupan 100%).
  - 4 Kasus Tidak Valid (*Negative Testing*): Tolak harga negatif, tolak kuantitas $\le 0$, tolak menu habis, tolak uang bayar kurang.
  - 3 Analisis Nilai Batas (*Boundary Value Analysis*): Uang pas (Rp50.000 $\rightarrow$ Rp0), uang lebih (Rp60.000 $\rightarrow$ Rp10.000), dan uang kurang (Rp40.000 $\rightarrow$ Ditolak).

---

## 5. Tiga Pertanyaan Kunci untuk Kelompok Penelaah (Design Review)
Berikut adalah 3 hal yang kami mintakan evaluasi dan tanggapannya dari rekan kelompok penelaah:
1. **Kenyamanan Alur POS:** *"Apakah tata letak dua kolom (grid katalog di sisi kiri dan keranjang belanja di sisi kanan) pada wireframe POS Kasir (`wf-02`) sudah cukup ergonomis dan cepat bagi kasir warung saat jam sibuk antrean makan siang?"*
2. **Pencegahan Human Error:** *"Apakah penonaktifan tombol 'Bayar' secara otomatis saat uang tunai kurang sudah cukup jelas sebagai umpan balik (*feedback*), ataukah diperlukan dialog konfirmasi tambahan?"*
3. **Pemisahan Kas Tunai vs QRIS:** *"Pada wireframe Laporan Omzet (`wf-06`), apakah pemisahan nominal fisik Kas Tunai vs Saldo QRIS di kartu metrik sudah memenuhi kebutuhan rekonsiliasi kas harian pemilik warung?"*
