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

### 🔹 Sprint 1 (Minggu 9–10): Fondasi Kerangka, CRUD Entitas, Relasi, dan Pencarian
- **Status:** ✅ **SELESAI 100% (Jobsheet 9 & Jobsheet 10)**
- **Fokus Utama:** Menyelesaikan kerangka berlapis Flask + SQLite, manajemen master data, relasi multi-tabel, pencarian aman, debugging, dan pengujian regresi.
- **Butir Backlog yang Diselesaikan:**
  - `T-1.1 & T-1.2`: Kerangka MVC Flask, `.venv`, `requirements.txt`, dan basis data SQLite `kasir_warung.db` dari `schema.sql` (Selesai pada JS 9).
  - `T-1.3 / KF-01`: Modul CRUD Menu lengkap (`GET /menu`, `POST /menu/tambah`, `POST /menu/<id>/ubah`, `POST /menu/<id>/hapus`) dengan validasi server (Selesai pada JS 9).
  - `KF-01 (Kategori)`: Modul CRUD Kategori dengan query agregasi jumlah hidangan dan proteksi foreign key (Selesai pada JS 9).
  - `G1 & KF-11`: Riwayat Transaksi Penjualan dengan JOIN 4 tabel (`transaksi`, `pengguna`, `detail_transaksi`, `menu`) dan kalkulasi total dinamis (Selesai pada JS 10).
  - `G2 & KF-10`: Form Catat Transaksi Baru dengan validasi masukan relasi induk-anak (Selesai pada JS 10).
  - `G3 & KNF-05`: Transaksi Atomik Multi-Tabel (`with koneksi()`) terbukti rollback 100% aman (Selesai pada JS 10).
  - `G4 / Pencarian & Filter`: Pencarian nama menu aman (`LIKE ? ESCAPE '\'`) dan filter gabungan kategori serta status (Selesai pada JS 10).
  - `Uji Cepat Regresi`: Suite pengujian otomatis terisolasi dengan basis data sementara di `tests/uji_cepat.py` (5/5 kategori lulus).
  - `Refactoring`: Ekstraksi helper `_render_menu_form()` di `app.py`.
- **Capaian Entri Jurnal:** 18 entri (termasuk 2 entri `[Debug]`) tercatat di `jurnal-vibe-coding.md`.

---

### 🔹 Sprint 2 (Minggu 11–12): Autentikasi Multi-Peran, Antarmuka, dan Hardening Keamanan
> ⭐ **TITIK PERIKSA CHECKPOINT DOSEN (MINGGU 12) — SELESAI 100%**
- **Status:** ✅ **SELESAI 100% (Jobsheet 11 & Jobsheet 12)**
- **Fokus Utama:** Autentikasi sesi, RBAC 2 peran (Pemilik vs Kasir), validasi masukan dua lapis, penyeragaman antarmuka wireframe, code review OWASP Top 10, dan mitigasi keamanan (CSRF, Rate Limiting, Audit Logging).
- **Butir Backlog yang Diselesaikan:**
  - `UC-01 / Pengguna`: Modul Login & Logout aman dengan password hash `scrypt` dan proteksi open redirect (Selesai pada JS 11).
  - `H3 / RBAC Server`: Decorator `@peran_diperlukan` di server; kasir diblokir HTTP 403 Forbidden pada rute manajerial menu & kategori (Selesai pada JS 11).
  - `H4 / Antarmuka Wireframe`: Satu berkas CSS terpusat `static/style.css`, layout `templates/base.html` adaptif, halaman ramah `403.html` dan `400.html` (Selesai pada JS 11 & 12).
  - `H5 / Validasi Dua Lapis`: Atribut HTML5 di peramban + validasi mutlak server di `services.py` (Selesai pada JS 11).
  - `T-01 / Proteksi CSRF`: Token sinkronisasi acak per sesi `secrets.token_hex(16)` di seluruh formulir POST (Selesai pada JS 12).
  - `T-02 & T-03 / Rate Limiter & Audit Logging`: Pembatasan 5 kali gagal per 5 menit (`percobaan.py` $\rightarrow$ HTTP 429) dan logging insiden keamanan tanpa kata sandi (Selesai pada JS 12).
  - `T-04 & T-05 / Hardening Produksi`: Header keamanan `nosniff`, `DENY`, `same-origin`, fail-secure `SECRET_KEY`, dan dependensi terkunci di `requirements.txt` (Selesai pada JS 12).
- **Capaian Entri Jurnal:** **30 entri lengkap** tercatat di `jurnal-vibe-coding.md` (Target semester RTM-2 terpenuhi).
- **Status Uji Regresi:** Suite otomatis di `tests/uji_cepat.py` mencakup seluruh alur dengan hasil **LULUS 100%**.

---

### 🔹 Sprint 3 (Minggu 13–14): Pengujian Otomatis, Perbaikan Cacat, dan Pelaksanaan UAT
- **Fokus Utama:** Penjaminan mutu perangkat lunak, perbaikan cacat nyata (Red-Green TDD), dan verifikasi operasional langsung dengan pemilik warung makan.
- **Capaian Minggu 13 (Jobsheet 13 — Selesai 100%):**
  - Matriks Keterlacakan & 28 Test Case black-box (BVA, EP, Negative) pada `docs/pengujian/test-case.md`.
  - Suite pengujian modern `pytest 9.1.1` (47 uji lulus 100%) mencakup validasi batas harga/porsi, matriks rute HTTP x 3 peran, dan alur transaksi kasir.
  - Penutupan dan perbaikan 3 cacat nyata (`D-01` porsi unicode, `D-02` harga raksasa anti overflow, `D-03` format tanggal ISO) di `services.py`.
  - Penyusunan dokumen rencana UAT (`docs/pengujian/rencana-uat.md`) berisi 6 skenario alur kerja nyata kasir.
  - Jadwal UAT disepakati bersama Pak Joko (Jumat, 27 November 2026 pukul 14.00 WIB).
  - Capaian Jurnal Vibe Coding: **38 entri lengkap** (bertambah 8 entri baru).
- **Target Minggu 14 (Pertemuan 14):**
  - Pelaksanaan sesi pengujian penerimaan pengguna (UAT) di Warung Makan Mitra.
  - Pengisian kuesioner evaluasi kegunaan sistem (SUS / usability questionnaire).
  - Rilis aplikasi versi `v1.0-release` beserta dokumentasi panduan pengguna (*user manual*).

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
