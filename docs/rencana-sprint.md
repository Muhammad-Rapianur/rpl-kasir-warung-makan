# Rencana Sprint Pengembangan Aplikasi (RTM-2) — KasirWarung

Dokumen ini memetakan rencana pelaksanaan 4 siklus *Sprint* untuk menyelesaikan tugas besar **RTM-2 (Implementasi Sistem & Laporan Bab 4)** pada mata kuliah Rekayasa Perangkat Lunak, D3 TI Politeknik Sampit.

---

## 1. Ikhtisar RTM-2 & Target Utama
- **Total Kebutuhan Fungsional (KF):** $\ge 10$ KF inti (KasirWarung memiliki 13 KF).
- **Total Kebutuhan Non-Fungsional (KNF):** $\ge 4$ KNF (Waktu muat $\le 2\text{ s}$, kalkulasi $\le 500\text{ ms}$, *offline-first*, font $\ge 16\text{ px}$).
- **Autentikasi & Otorisasi:** Minimal 2 peran (*Kasir* dan *Pemilik Warung*).
- **Target Jurnal Vibe Coding:** $\ge 30$ entri pada akhir semester.
- **Rangkaian Pengujian:** $\ge 20$ Test Case ($\ge 8$ pengujian otomatis) dan UAT dengan pemilik warung.

---

## 2. Peta Jalan Sprint (Sprint Roadmap)

```
[Sprint 1: Minggu 9–10]  ──> Kerangka, CRUD Menu & Kategori, Relasi, Filter/Pencarian
           │
[Sprint 2: Minggu 11–12] ──> Autentikasi 2 Peran, Layar POS Kasir, Checkpoint Minggu 12 ⭐
           │
[Sprint 3: Minggu 13–14] ──> Logika Transaksi, Hitung Kembalian, Cetak Struk, UAT Klien
           │
[Sprint 4: Minggu 15–16] ──> Rekap Omzet, Top 5 Menu, Laporan Bab 4, Demo Final UAS 🚀
```

---

## 3. Rincian Alokasi Fitur per Sprint

### 🔹 Sprint 1 (Minggu 9–10): Fondasi Kerangka, CRUD Entitas, dan Relasi
- **Fokus Utama:** Menyelesaikan kerangka berlapis Flask + SQLite dan manajemen master data.
- **Butir Backlog yang Diselesaikan:**
  - `T-1.1 & T-1.2`: Kerangka MVC Flask, `.venv`, `requirements.txt`, dan koneksi basis data SQLite `kasir_warung.db` dari `schema.sql` (Selesai pada JS 9).
  - `T-1.3 / KF-01`: Modul CRUD Menu lengkap (`GET /menu`, `POST /menu/tambah`, `POST /menu/<id>/ubah`, `POST /menu/<id>/hapus`) dengan validasi server (Selesai pada JS 9).
  - `KF-01 (Kategori)`: Modul CRUD Kategori dengan query agregasi jumlah hidangan dan proteksi foreign key (Selesai pada JS 9).
  - **Pekerjaan Minggu Depan (Pertemuan 10):**
    - Fitur pencarian (*search bar*) nama menu dan penyaringan (*filtering*) hidangan berdasarkan kategori di layar kasir.
- **Target Entri Jurnal:** Minimal 12 entri.

---

### 🔹 Sprint 2 (Minggu 11–12): Autentikasi Multi-Peran & Layar Transaksi Kasir
> ⭐ **TITIK PERIKSA CHECKPOINT DOSEN (MINGGU 12)**
- **Fokus Utama:** Hak akses pengguna dan perakitan komponen utama POS kasir.
- **Butir Backlog yang Dikerjakan:**
  - `UC-01 / Pengguna`: Modul Login & Session autentikasi 2 peran (*Kasir* vs *Pemilik Warung*).
  - `KF-01 & KF-03`: Integrasi katalog tombol menu layar sentuh dan pemilihan tipe pesanan (*Dine-in / Take-away*).
  - `KF-04`: Logika keranjang belanja kasir *real-time* via JavaScript/Fetch API lokal.
  - `KF-05`: Pencegahan pemesanan menu yang berstatus *Habis*.
  - **Tinjauan Keamanan & Code Review:** Audit celah keamanan sesi login, sanitasi input, dan rotasi acak `SECRET_KEY`.
- **Target Entri Jurnal:** Minimal 20 entri.

---

### 🔹 Sprint 3 (Minggu 13–14): Pembayaran, Struk, dan Pengujian Lapangan (UAT)
- **Fokus Utama:** Penyelesaian alur pembayaran dan verifikasi langsung dengan klien.
- **Butir Backlog yang Dikerjakan:**
  - `KF-06 & KF-07`: Kalkulasi otomatis uang kembalian tunai dan penolakan transaksi uang kurang.
  - `KF-08`: Pilihan metode bayar Tunai vs QRIS statis warung.
  - `KF-09`: Penomoran nota transaksi unik urut harian (`TRX-YYYYMMDD-XXX`).
  - `KF-10`: Template cetak nota peramban `@media print` format thermal 58mm/80mm.
  - `KF-11`: Halaman riwayat transaksi harian dan aksi cetak ulang nota.
  - **Eksekusi Pengujian:** Menjalankan 17 Test Case terukur (`rencana-uji.md`) dan sesi *User Acceptance Testing* (UAT) bersama kasir warung makan.
- **Target Entri Jurnal:** Minimal 26 entri.

---

### 🔹 Sprint 4 (Minggu 15–16): Rekapitulasi Omzet, Finalisasi Bab 4, dan Demo UAS
- **Fokus Utama:** Modul manajerial pemilik, pembukuan kas, dan pelaporan akhir.
- **Butir Backlog yang Dikerjakan:**
  - `KF-12`: Laporan rekapitulasi omzet harian: pemisahan otomatis uang Kas Tunai fisik vs Saldo masuk QRIS.
  - `KF-13`: Visualisasi 5 menu paling laris (*Top 5 Best Sellers*) hari berjalan.
  - `README.md & User Manual`: Penyusunan panduan instalasi dan pengoperasian kasir.
  - **Penyusunan Laporan Bab 4:** Implementasi kode, hasil pengujian, dan analisis efektivitas *Vibe Coding Terkendali* dari data jurnal.
  - **Demo Sistem (UAS):** Demonstrasi kelancaran operasional kasir secara *offline-first*.
- **Target Entri Jurnal:** $\ge 30$ entri (Target RPS terpenuhi).

---

## 4. Pembagian Tugas Tim (Pair Programming Pertemuan 10)

| Anggota Tim | Peran Sprint 1 (Lanjutan) | Fokus Tugas Pertemuan 10 |
| :--- | :--- | :--- |
| **Muhammad Rapianur** | *Driver / Backend Engineer* | Implementasi API endpoint filter kategori dan pencarian menu cepat (`GET /api/menu?kategori=...&q=...`). |
| **Rekan Kelompok** | *Navigator / Frontend & Test* | Integrasi tab filter kategori di antarmuka web dan penulisan skrip pengujian pencarian di `tests/`. |

---

*Disahkan untuk pedoman eksekusi RTM-2 Rekayasa Perangkat Lunak.*
