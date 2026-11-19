# Rangkuman Bahan Bab 4: Pengujian, Evaluasi, dan Rilis Sistem (KasirWarung)

> **Proyek:** Sistem Informasi Kasir Warung Makan (KasirWarung v1.0.0)  
> **Mahasiswa:** Muhammad Rapianur (NIM: 24554010004)  
> **Program Studi:** D3 Teknologi Informasi, Politeknik Sampit  
> **Mata Kuliah:** Rekayasa Perangkat Lunak  

Dokumen ini menghimpun seluruh data empiris, hasil pengujian perangkat lunak, evaluasi penerimaan pengguna, serta analisis proses rekayasa (*Vibe Coding*) sebagai materi penyusunan **Bab 4 (Hasil dan Pembahasan)** pada Laporan Akhir Proyek.

---

## 1. Rangkuman Pengujian Perangkat Lunak

### 1.1 Pengujian Black-Box (Equivalence Partitioning & Boundary Value Analysis)
Berdasarkan dokumen `docs/pengujian/test-case.md`, telah dirumuskan dan diuji sebanyak **28 Kasus Uji Fungsional**:
- **Cakupan Modul:** Otentikasi Pengguna (TC-LOG), Pengelolaan Menu (TC-MNU), Pengelolaan Kategori (TC-KAT), Transaksi Penjualan (TC-TRX), dan Kontrol Akses Peran (TC-RBAC).
- **Hasil Pengujian Aktual:** **28 / 28 Kasus Uji Lulus (100% Passed)** setelah dilakukan pengerasan validasi masukan.

### 1.2 Pengujian Otomatis (Pytest & Uji Regresi Keamanan)
- **Suite Uji Pytest Modern (`pytest 9.1.1`):** **53 fungsi uji otomatis LULUS 100%** (eksekusi dalam 1.57 detik).
  - 33 kasus pengujian batas nilai (BVA) dan partisi ekuivalen (EP) masukan numerik & tanggal.
  - 8 kasus matriks otorisasi rute HTTP x 3 peranan (Tamu, Kasir, Pemilik).
  - 5 kasus pengujian alur integrasi transaksi kasir multi-item.
  - 6 kasus pengujian kebersihan rilis (`test_rilis.py`).
  - 1 kasus uji smoke dasar.
- **Suite Uji Regresi Keamanan Cepat (`tests/uji_cepat.py`):** **9 modul uji keamanan LULUS 100%** (Proteksi CSRF, Anti-Brute Force HTTP 429, Password Hash scrypt, Anti-Open Redirect, RBAC 403, dan Security Headers).

---

## 2. Rangkuman Pelaporan dan Perbaikan Cacat (Defect Tracking)

Selama pengujian sistem pada Sprint 3, teridentifikasi 3 cacat perangkat lunak yang berhasil diperbaiki secara tuntas pada file `services.py` (tercatat di `docs/pengujian/laporan-cacat.md`):

| ID Cacat | Deskripsi Kerentanan / Cacat | Klasifikasi Tingkat | Tindakan Rekayasa / Perbaikan | Status Akhir |
|:---:|---|:---:|---|:---:|
| **D-01** | Angka Unicode (contoh: karakter pangkat dua '²') meloloskan fungsi `isdigit()`, memicu galat 500 saat konversi `int()`. | Sedang (*Medium*) | Hardening filter validasi ketat menggunakan kombinasi `teks.isascii() and teks.isdigit()`. | **Tuntas / Diperbaiki** |
| **D-02** | Integer Overflow pada harga hidangan dan porsi kuantitas jika menerima masukan ekstrem (30 digit angka). | Tinggi (*High*) | Pembatasan batas atas angka `BATAS_ANGKA = 1_000_000_000` dan panjang karakter `len <= 10`. | **Tuntas / Diperbaiki** |
| **D-03** | Inkonsistensi format tanggal ISO pada Python 3.11+ yang meloloskan tanggal tanpa tanda hubung (`20261120`). | Rendah (*Low*) | Penerapan pola regex baku `re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tanggal)`. | **Tuntas / Diperbaiki** |

---

## 3. Rangkuman Hasil User Acceptance Testing (UAT) dan Evaluasi SUS

Pengujian penerimaan pengguna dilaksanakan pada **20 November 2026** melibatkan Pemilik Warung Makan dan Petugas Kasir dengan hasil:
- **Tingkat Kelulusan Skenario:** **6 dari 6 Skenario Inti Lulus 100% (6/6)**.
- **Skor System Usability Scale (SUS):**
  - Responden 1 (Pemilik Warung): **87.5 / 100**
  - Responden 2 (Petugas Kasir): **97.5 / 100**
  - **Skor Rata-rata SUS:** **92.5 / 100**
  - **Kategori Kelayakan Usabilitas:** **Grade A (Excellent / Sangat Layak Pakai)**.
- **Triase Umpan Balik:**
  - 1 temuan kesulitan antarmuka (penjelasan tombol reset) ditindaklanjuti pada manual pengguna.
  - 2 usulan fitur baru (printer thermal dan ekspor excel) dialokasikan untuk roadmap versi berikutnya (v1.1).
  - Status rilis disetujui penuh (*Accepted*) tanpa cacat blokir.

---

## 4. Analisis Metrik Jurnal Rekayasa (Vibe Coding Analysis)

Proses perancangan dan implementasi perangkat lunak menggunakan bantuan asisten AI didokumentasikan secara ketat dalam **46 siklus rekayasa** pada `jurnal-vibe-coding.md`:

```text
Distribusi Keputusan Iterasi Vibe Coding:
├── Diterima (Terima) : 43 siklus (93,5%)
├── Diubah   (Ubah)   :  3 siklus ( 6,5%)
└── Ditolak  (Tolak)  :  0 siklus ( 0,0%)
Total Siklus Rekayasa : 46 siklus
Sesi Khusus Debugging :  3 sesi (Siklus 8, 17, 43)
```

### Temuan Pembelajaran Rekayasa (*Engineering Insights*):
1. **Pengendalian Halusinasi AI:** Pemberian konteks spesifikasi yang ketat (*tight context*) dan batasan domain warung makan secara eksplisit berhasil menekan tingkat penolakan kode AI hingga 0%.
2. **Koreksi Kritis Mandiri:** Sebanyak 6,5% perubahan manual dilakukan pengembang untuk mengatasi limitasi bawaan AI, khususnya pada:
   - Penyesuaian pemformatan mata uang lokal Indonesia (Rupiah).
   - Penyelarasan docstring dan penanganan sintaks Python 3.14.
   - Penanganan perbedaan encoding berkas Windows (UTF-16 LE BOM) pada file konfigurasi dependensi rilis (`requirements.txt`).
3. **Pemberdayaan Uji Otomatis:** Otomasi pengujian (`pytest`) bertindak sebagai verifikator objektif utama untuk menapis output AI yang menghasilkan *false green* sebelum kode diintegrasikan ke cabang utama.

---

*Disusun secara otomatis untuk lampiran Bab 4 Laporan Tugas Akhir / Praktikum RPL 2026.*
