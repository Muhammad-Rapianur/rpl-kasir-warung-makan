# Laporan Cacat & Pengujian Eksploratif — KasirWarung
**Proyek:** Sistem Informasi Kasir Warung Makan (`rpl-kasir-warung-makan`)  
**Penyusun:** Muhammad Rapianur (NIM: 24554010004)  
**Mata Kuliah:** Rekayasa Perangkat Lunak — Praktikum 13 (Tugas Lab 12)  
**Tanggal:** 20 November 2026  
**Status Dokumen:** Selesai Diperbaiki (Langkah 11 — Semua Cacat Tertutup)  

---

## 1. Daftar Cacat Nyata (Defects)

### D-01: Karakter Angka Unicode pada Kuantitas Porsi Menyebabkan Galat 500
* **Ditemukan:** 20 November 2026 oleh Muhammad Rapianur lewat TC-12 & uji eksploratif form transaksi kasir.
* **Langkah Reproduksi:**
  1. Masuk (*login*) sebagai kasir (`kasir_siti`).
  2. Buka menu pencatatan transaksi baru (`GET /transaksi/tambah`).
  3. Masukkan jumlah porsi hidangan dengan karakter Unicode superscript: `jumlah = "²"`.
  4. Klik tombol **Simpan Transaksi**.
* **Hasil Aktual:** Aplikasi melempar exception `ValueError: invalid literal for int() with base 10: '²'` pada baris `services.py:111`, menyebabkan peramban menerima galat 500 Internal Server Error.
* **Hasil Diharapkan:** Ditolak dengan pesan validasi ramah: *"Jumlah porsi harus berupa angka lebih dari 0"*.
* **Keparahan:** **Sedang** (Permintaan gagal memproses dan memicu uncaught exception, namun tidak merusak integritas basis data).
* **Prioritas:** **Sprint Ini**
* **Akar Penyebab:** Fungsi `str.isdigit()` bawaan Python mengembalikan nilai `True` untuk karakter angka Unicode (seperti `²`, `³`, `٩`), tetapi fungsi `int()` standar Python gagal mengonversinya ke basis 10.
* **Perbaikan:** Menambahkan pengecekan `teks.isascii() and teks.isdigit()` pada fungsi validasi angka di `services.py`. Uji regresi: `tests/test_validasi.py::test_validasi_jumlah_porsi_transaksi['²'-False]`.
* **Status:** **Diperbaiki**

---

### D-02: Harga Menu Makanan Raksasa (30 Digit) Lolos Validasi dan Memicu OverflowError Basis Data
* **Ditemukan:** 20 November 2026 oleh Muhammad Rapianur lewat TC-10 & TC-11 pada validasi harga menu.
* **Langkah Reproduksi:**
  1. Masuk sebagai pemilik (`pak_pemilik`).
  2. Buka form tambah menu (`GET /menu/tambah`).
  3. Isi nama hidangan: `"Nasi Tumpeng Spesial"`, kategori: `"1"`.
  4. Isi harga jual dengan 30 digit angka sembilan: `harga = "999999999999999999999999999999"`.
  5. Kirim formulir via POST.
* **Hasil Aktual:** Validasi di `services.py` meloloskan input karena hanya memeriksa `int(teks) > 0`. Saat dieksekusi kueri SQL di `models.py`, driver SQLite melempar exception fatal: `OverflowError: Python int too large to convert to SQLite INTEGER` (Galat 500).
* **Hasil Diharapkan:** Ditolak di lapisan logika bisnis (`services.py`) dengan pesan: *"Harga jual harus berupa bilangan bulat positif lebih besar dari 0 dan maksimal Rp 1.000.000.000"*.
* **Keparahan:** **Sedang** (Menyebabkan crash pada sisi server saat melakukan operasi tulis ke database).
* **Prioritas:** **Sprint Ini**
* **Akar Penyebab:** Ketiadaan batasan nilai maksimum (*upper bound*) dan panjang digit string pada fungsi `_bilangan_positif()` di `services.py`.
* **Perbaikan:** Menetapkan konstanta `BATAS_ANGKA = 1_000_000_000` (1 Miliar Rupiah) dan batas panjang string maksimal 10 digit pada `services.py`. Uji regresi: `tests/test_validasi.py::test_validasi_harga_menu[1000000001-False]` dan `test_validasi_harga_menu[999999999999999999999999999999-False]`.
* **Status:** **Diperbaiki**

---

### D-03: Masukan Format Tanggal Tanpa Pemisah Tanda Hubung Diterima Sistem
* **Ditemukan:** 20 November 2026 oleh Muhammad Rapianur lewat uji BVA/EP pada tanggal transaksi.
* **Langkah Reproduksi:**
  1. Masuk sebagai kasir.
  2. Buka form catat transaksi (`GET /transaksi/tambah`).
  3. Masukkan tanggal transaksi dalam bentuk 8 digit rapat: `tanggal = "20261120"`.
  4. Kirim form POST.
* **Hasil Aktual:** Nilai string `"20261120"` dianggap valid dan diterima oleh fungsi bawaan `date.fromisoformat()` pada Python 3.11+, lalu disimpan ke basis data sebagai `2026-11-20`.
* **Hasil Diharapkan:** Ditolak dengan pesan peringatan: *"Tanggal harus berformat TTTT-BB-HH (contoh: 2026-11-20)"* sesuai spesifikasi PRD & kamus data SRS kasir warung makan.
* **Keparahan:** **Rendah** (Data tanggal tidak rusak karena terkonversi, namun melanggar aturan format input dokumen spesifikasi).
* **Prioritas:** **Sprint Ini**
* **Akar Penyebab:** Perilaku baru `date.fromisoformat()` pada Python 3.11+ yang lebih longgar menerima format tanggal ISO tanpa pemisah tanda hubung (*basic format* `YYYYMMDD`).
* **Perbaikan:** Menambahkan pemeriksaan ekspresi reguler `re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", tanggal)` sebelum memanggil `fromisoformat()` di `services.py`. Uji regresi: `tests/test_validasi.py::test_validasi_tanggal_transaksi[20261120-False]`.
* **Status:** **Diperbaiki**

---

## 2. Daftar Permintaan Perubahan (Change Requests — Terpisah dari Cacat)

Sesuai arahan Jobsheet 13 Bagian 2.5, perbedaan preferensi bisnis yang bukan pelanggaran PRD dicatat sebagai Permintaan Perubahan:

| ID CR | Modul | Deskripsi Usulan Klien Warung | Keputusan Bersama |
|:---:|:---|:---|:---|
| **CR-01** | Pengelolaan Menu | Penolakan nama menu ganda yang hanya berbeda huruf besar/kecil (misal: `"Ayam Bakar"` dan `"ayam bakar"` dianggap sama). | **Diterima untuk Sprint 3:** Ditambahkan validasi `LOWER(nama)` unik agar menu tidak terduplikasi secara visual di daftar pesanan kasir. |
| **CR-02** | Transaksi Kasir | Opsi pembulatan uang kembalian receh (pecahan di bawah Rp 500) menjadi diskon atau donasi sukarela warung. | **Ditunda (Won't Have Sprint ini):** Klien menyepakati kasir tetap menginput angka uang diterima aktual secara manual. |
