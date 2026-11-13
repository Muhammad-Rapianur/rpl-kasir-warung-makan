# Rencana Pengujian Sistem (Test Plan) — KasirWarung
## Dokumen Perencanaan dan Pengujian Perangkat Lunak (Jobsheet 7)

---

### Informasi Dokumen
- **Nama Proyek:** Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*)
- **Mata Kuliah:** Rekayasa Perangkat Lunak (RPL)
- **Fase Pengujian:** Verifikasi Rancangan (Minggu 7) & Eksekusi Pengujian (Minggu 13–14)
- **Penyusun:** Tim Pengembang KasirWarung

---

## 1. Tujuan dan Ruang Lingkup

### 1.1 Tujuan Pengujian
1. Memastikan seluruh fungsi operasional kasir (pemilihan menu, perhitungan subtotal, kalkulasi kembalian, cetak struk nota, dan rekapitulasi omzet) bekerja akurat sesuai spesifikasi kebutuhan di [SRS Ringkas](../srs/srs.md) dan kriteria penerimaan di [PRD.md](../../PRD.md).
2. Memverifikasi keandalan sistem dalam menangani kondisi perkecualian (*edge cases* dan kasus tidak valid), seperti menu yang habis dipesan atau uang tunai yang dibayarkan kurang.
3. Menjamin sistem aman dari kesalahan input matematis dan celah integritas data sebelum diimplementasikan di warung makan klien.

### 1.2 Ruang Lingkup Kebutuhan yang Diuji
Pengujian mencakup seluruh kebutuhan fungsional dan non-fungsional proyek:
- **Kebutuhan Must Have:**
  - `KF-01`: Menampilkan katalog menu dan kategori.
  - `KF-02`: Manajemen menu dan status ketersediaan (*Tersedia / Habis*).
  - `KF-03`: Pilihan tipe pesanan *Dine-in* (dengan nomor meja) atau *Bungkus (Take-away)*.
  - `KF-04`: Kalkulasi subtotal tiap menu dan total belanja otomatis.
  - `KF-05`: Penolakan pemesanan menu yang berstatus habis.
  - `KF-06` & `KF-07`: Kalkulasi uang kembalian tunai dan penolakan transaksi jika uang tunai kurang.
  - `KF-08`: Pemilihan metode pembayaran Tunai dan QRIS statis.
  - `KF-09`: Pembuatan nomor transaksi unik (`TRX-YYYYMMDD-XXX`) dan penyimpanan persisten.
  - `KF-12`: Rekapitulasi omzet harian dengan pemisahan kas Tunai fisik vs saldo QRIS.
- **Kebutuhan Should Have:**
  - `KF-10`: Format tampilan cetak struk nota printer thermal 58mm/80mm.
  - `KF-11`: Riwayat transaksi penjualan harian.
  - `KF-13`: Ringkasan 5 menu makanan/minuman paling laris (*Top 5 Best Seller*).
- **Kebutuhan Non-Fungsional (KNF):**
  - `KNF-01` & `KNF-02`: Waktu muat halaman $\le 2\text{ detik}$ dan kalkulasi keranjang $\le 500\text{ ms}$.
  - `KNF-03`: Keandalan sistem beroperasi penuh secara lokal tanpa internet (*offline-first*).
  - `KNF-05`: Ukuran teks harga dan tombol kasir $\ge 16\text{ px}$ (keterbacaan visual).
  - `KNF-06`: Validasi server menolak harga dan kuantitas bernilai negatif.

---

## 2. Strategi Pengujian (Test Strategy)

Pengujian sistem dilaksanakan melalui 3 tingkatan strategi terpadu:

1. **Pengujian Black-Box Manual (*Functional Black-Box Testing*):**
   - Dilakukan oleh tim pengembang untuk menguji antarmuka web peramban dari sudut pandang pengguna akhir (kasir dan pemilik).
   - Memfokuskan pengujian pada masukan (*input*) dan keluaran (*output*) berdasarkan teknik **Partisi Ekuivalen (*Equivalence Partitioning*)** dan **Analisis Nilai Batas (*Boundary Value Analysis*)**.
2. **Pengujian Otomatis Logika Inti (*Automated Unit Testing* — Minggu 13):**
   - Menguji fungsi-fungsi bisnis kritis di `services.py` dan `models.py` menggunakan framework uji Python bawaan (`unittest` / `pytest`).
   - Meliputi otomatisasi pengujian fungsi kalkulasi harga, validasi logika kembalian, dan pengujian integritas batasan basis data (`tests/cek_skema.py`).
3. **Pengujian Penerimaan Pengguna (*User Acceptance Testing / UAT* — Minggu 13–14):**
   - Melibatkan pemilik dan kasir warung makan secara langsung di meja kasir.
   - Menguji apakah alur kerja sistem terasa mudah dipahami, tidak memperlambat antrean makan siang, dan hasil cetak struk pas pada printer thermal fisik warung.

---

## 3. Lingkungan dan Data Uji (Test Environment)

### 3.1 Spesifikasi Perangkat Keras & Lunak
- **Perangkat Keras:** Laptop standar pengembang / kasir (RAM minimal 4 GB), monitor resolusi $1366 \times 768$ piksel, printer thermal USB/Bluetooth lebar 58mm.
- **Sistem Operasi:** Windows 10/11 Home/Pro (64-bit).
- **Peramban Web (*Browser*):** Google Chrome versi 120+ dan Microsoft Edge terbaru.
- **Basis Data:** SQLite 3 (berkas lokal `kasir_warung.db` dengan `PRAGMA foreign_keys = ON;`).

### 3.2 Data Uji (*Test Data*)
Sesuai prinsip etika kerja Jobsheet 7, pengujian **hanya menggunakan data karangan (*dummy data*)** dan dilarang memuat data pribadi narasumber:
- Akun Kasir Uji: `username: kasir_test`, `password: password123`.
- Akun Pemilik Uji: `username: owner_test`, `password: password123`.
- Data Menu Uji: *Nasi Putih (Rp4.000, Tersedia)*, *Ayam Goreng (Rp15.000, Tersedia)*, *Ayam Bakar (Rp18.000, Habis)*, *Es Teh Manis (Rp5.000, Tersedia)*.
- Nomor Meja Uji: Meja 01 s.d. Meja 10.

---

## 4. Kriteria Kelulusan Pengujian (Pass/Fail Criteria)

Sistem perangkat lunak dinyatakan **LULUS UJI** dan siap diserahterimakan apabila memenuhi ketentuan berikut:

1. **Tingkat Keterpenuhan (*Test Pass Rate*):**
   - **100% test case berkategori Must Have** wajib berstatus **LULUS (PASS)** tanpa pengecualian.
   - Minimal **90% test case berkategori Should Have** berstatus **LULUS (PASS)**.
2. **Kriteria Tingkat Keparahan Cacat (*Defect Severity Threshold*):**
   - **Cacat Kritis (*Severity 1 - Blocker*):** **Toleransi = 0**. (Contoh: salah menghitung uang kembalian, aplikasi crash saat menyimpan transaksi, database rusak).
   - **Cacat Sedang (*Severity 2 - Major*):** **Toleransi = 0** pada rilis final. (Contoh: format struk terpotong pada cetakan printer thermal, filter tanggal meleset).
   - **Cacat Ringan (*Severity 3 - Minor*):** Toleransi maksimal 2 temuan kosmetik minor yang tidak menghalangi proses penjualan kasir.

---

## 5. Pembagian Peran dan Tugas Penguji

| No | Nama Anggota Tim | Peran Pengujian | Fokus Modul yang Diuji |
| :-: | :--- | :--- | :--- |
| 1 | **Anggota 1** | Lead Tester (Kasir & Alur Transaksi) | Pengujian modul login (`UC-01`), keranjang belanja POS, kalkulasi subtotal otomatis, dan validasi menu habis (`KF-01` s.d. `KF-05`). |
| 2 | **Anggota 2** | Tester Pembayaran & Struk Nota | Pengujian perhitungan uang kembalian tunai, penolakan uang kurang, verifikasi QRIS, nomor transaksi unik, dan dialog cetak struk thermal (`KF-06` s.d. `KF-10`). |
| 3 | **Anggota 3** | Tester Manajerial & Kinerja Basis Data | Pengujian modul CRUD menu pemilik, rekapitulasi omzet harian, menu terlaris, pengujian integritas batasan SQL, dan uji kecepatan muat halaman (`KF-11` s.d. `KF-13`, KNF). |

---

## 6. Daftar Test Case Awal (Langkah 8)

Daftar pengujian disusun berdasarkan kriteria penerimaan pada PRD dan Kebutuhan Fungsional (KF) di SRS. Setiap kasus uji memiliki hasil terukur (*measurable*), mencakup kelas data valid, kasus tidak valid, serta analisis nilai batas (*Boundary Value Analysis*).

| ID Test Case | KF yang Diuji | Prasyarat & Data Uji | Langkah-langkah Pengujian | Hasil yang Diharapkan (Terukur) | Teknik Pengujian |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **TC-01** | **KF-01** | Kasir login aktif. Database memuat menu kategori Makanan, Minuman, dll. | 1. Buka halaman utama POS Kasir (`wf-02`).<br>2. Klik tab filter kategori 'Minuman'. | Sistem menampilkan seluruh menu minuman berstatus aktif dengan nama dan harga satuan sesuai database dalam waktu $\le 2\text{ detik}$. | Partisi Valid |
| **TC-02** | **KF-02** | Pemilik login aktif di halaman Kelola Menu (`wf-04`). | 1. Klik '+ Tambah Menu Baru'.<br>2. Isi Nama='Bebek Goreng', Kategori='Sayur & Lauk', Harga=25000.<br>3. Klik 'Simpan'. | Sistem menyimpan data ke tabel `menu`, memunculkan notifikasi hijau *"Menu berhasil ditambahkan"*, dan menu muncul di daftar. | Partisi Valid |
| **TC-03** | **KF-02** | Pemilik membuka form tambah menu. Data: Harga = -5000 (negatif). | 1. Isi Nama='Menu Cacat', Harga=-5000.<br>2. Klik tombol 'Simpan'. | **Ditolak.** Sistem memunculkan pesan validasi *"Harga menu harus berupa angka positif"*, data tidak disimpan ke basis data SQLite. | **Kasus Tidak Valid** (Nilai Batas Bawah) |
| **TC-04** | **KF-02** | Menu 'Ayam Bakar' berstatus 'tersedia'. | 1. Buka halaman Kelola Menu (`wf-04`).<br>2. Klik toggle status 'Ayam Bakar' menjadi 'Habis'. | Status di database berubah menjadi `'habis'`, muncul notifikasi *"Status menu berhasil diubah menjadi: HABIS"*, dan tombol menu di layar kasir otomatis *disabled*. | Partisi Valid |
| **TC-05** | **KF-03** | Kasir berada di halaman POS Kasir (`wf-02`). | 1. Pilih dropdown tipe pesanan 'Makan di Tempat'.<br>2. Masukkan nomor meja '05'. | Input nomor meja aktif dan data `tipe_pesanan='dine_in'` serta `nomor_meja='05'` siap disimpan ke transaksi. | Partisi Valid |
| **TC-06** | **KF-04** | Keranjang belanja kasir kosong. Menu: Nasi Putih (Rp4.000), Ayam Goreng (Rp15.000). | 1. Klik tombol 'Nasi Putih' (2x).<br>2. Klik tombol 'Ayam Goreng' (1x). | Subtotal Nasi Putih = Rp8.000, Subtotal Ayam Goreng = Rp15.000, Total Tagihan = **Rp23.000** dihitung otomatis seketika ($<500\text{ ms}$). | Partisi Valid |
| **TC-07** | **KF-04** | Keranjang belanja berisi 1x Nasi Putih. | 1. Ubah jumlah kuantitas menjadi 0 atau angka negatif (-1).<br>2. Tekan Enter / Simpan. | **Ditolak.** Sistem menolak angka $\le 0$, kuantitas otomatis kembali ke nilai minimal 1 porsi, dan total belanja tidak bernilai minus. | **Kasus Tidak Valid** (Nilai Batas) |
| **TC-08** | **KF-05** | Menu 'Ayam Bakar' berstatus 'habis' di etalase. | 1. Kasir mencoba menekan tombol kartu menu 'Ayam Bakar' di grid POS. | **Ditolak.** Item tidak masuk ke keranjang pesanan. Sistem memunculkan banner peringatan *"Menu Ayam Bakar sedang HABIS dan tidak dapat ditambahkan!"*. | **Kasus Tidak Valid** |
| **TC-09** | **KF-06** | Total tagihan belanja = Rp50.000. Data: Uang Tunai Diterima = **Rp50.000** (Uang Pas). | 1. Pilih metode 'Tunai'.<br>2. Input uang diterima Rp50.000.<br>3. Klik 'Bayar & Simpan'. | Transaksi berhasil disimpan ke database. Kembalian dihitung dan ditampilkan tepat **Rp0**. | **Nilai Batas** (Tepat Batas) |
| **TC-10** | **KF-06** | Total tagihan belanja = Rp50.000. Data: Uang Tunai Diterima = **Rp60.000** (Uang Lebih). | 1. Pilih metode 'Tunai'.<br>2. Input uang diterima Rp60.000.<br>3. Klik 'Bayar & Simpan'. | Transaksi berhasil disimpan ke database. Kembalian dihitung dan ditampilkan tepat **Rp10.000**. | **Nilai Batas** (Di Atas Batas) |
| **TC-11** | **KF-07** | Total tagihan belanja = Rp50.000. Data: Uang Tunai Diterima = **Rp40.000** (Uang Kurang). | 1. Pilih metode 'Tunai'.<br>2. Input uang diterima Rp40.000.<br>3. Klik tombol 'Bayar & Simpan'. | **Ditolak.** Sistem memunculkan pesan merah *"Nominal uang bayar kurang dari total belanja!"*, dan tombol Simpan Transaksi terkunci (*disabled*). | **Kasus Tidak Valid** (Nilai Batas Bawah) |
| **TC-12** | **KF-08** | Total belanja = Rp35.000. Metode bayar yang dipilih: QRIS. | 1. Pilih radio button 'QRIS'.<br>2. Kasir verifikasi bukti transfer pelanggan.<br>3. Klik 'Bayar & Simpan'. | Transaksi tersimpan dengan `metode_pembayaran='qris'`, kolom `uang_diterima=35000`, kembalian Rp0 tanpa perlu kalkulasi uang tunai. | Partisi Valid |
| **TC-13** | **KF-09** | Dua transaksi diselesaikan berurutan pada tanggal 14 November 2026. | 1. Selesaikan transaksi 1.<br>2. Selesaikan transaksi 2. | Transaksi 1 menghasilkan nomor unik `TRX-20261114-001`. Transaksi 2 menghasilkan `TRX-20261114-002` secara urut tanpa tumpang tindih (*UNIQUE*). | Partisi Valid |
| **TC-14** | **KF-10** | Transaksi `TRX-20261114-003` berhasil disimpan. | 1. Masuk ke halaman pratinjau struk (`wf-03`).<br>2. Klik tombol 'Cetak Nota (Thermal 58mm)'. | Dialog cetak peramban terbuka dengan styling thermal 58mm pas tanpa terpotong, memuat nama warung, nomor nota, rincian menu, total, dan kembalian. | Partisi Valid |
| **TC-15** | **KF-11** | Hari ini telah terjadi 3 transaksi penjualan. | 1. Buka halaman Riwayat Transaksi (`wf-05`).<br>2. Periksa tabel transaksi. | Sistem menampilkan tabel berisi 3 baris transaksi hari ini dengan rincian nomor nota, jam, kasir, meja, metode, dan total tagihan yang akurat. | Partisi Valid |
| **TC-16** | **KF-12** | Transaksi hari ini: Tunai Rp1.300.000 dan QRIS Rp550.000. | 1. Pemilik membuka halaman Laporan Omzet (`wf-06`).<br>2. Pilih tanggal hari ini dan klik 'Tampilkan'. | Kartu ringkasan menampilkan: Total Omzet = **Rp1.850.000**, Kas Tunai = **Rp1.300.000**, dan Saldo QRIS = **Rp550.000** secara akurat 100%. | Partisi Valid |
| **TC-17** | **KF-13** | Penjualan hari ini: Ayam Goreng terjual 35 porsi (terbanyak). | 1. Pemilik membuka halaman Laporan Omzet (`wf-06`).<br>2. Lihat tabel '5 Menu Paling Laris'. | Menu 'Ayam Goreng' tampil di peringkat #1 dengan total penjualan 35 porsi dan akumulasi omzet Rp525.000. | Partisi Valid |

---

## 7. Catatan Evaluasi Kesalahan AI yang Ditemukan (Langkah 8)

Sesuai instruksi Langkah 8 Jobsheet 7 untuk memeriksa dan memperbaiki draf awal buatan AI:

1. **Kesalahan Penambahan Fitur Fiktif oleh AI:**
   - *Temuan:* Pada draf awal, AI sempat mengusulkan test case untuk pengujian *pemindai barcode nirkabel* dan *integrasi pembayaran otomatis API GoPay/OVO*.
   - *Tindakan Perbaikan:* Ditolak dan dihapus karena fitur tersebut berstatus *Won't Have* pada SRS dan PRD warung makan klien.
2. **Hasil yang Diharapkan Tidak Terukur:**
   - *Temuan:* AI sering menulis hasil yang diharapkan dengan kalimat samar, seperti *"Sistem memproses transaksi dengan baik dan lancar"*.
   - *Tindakan Perbaikan:* Seluruh hasil yang diharapkan diubah menjadi parameter konkret dan terukur (contoh: *"Kembalian dihitung tepat Rp10.000"*, *"Sistem memunculkan pesan peringatan merah 'Nominal uang bayar kurang!' dan tombol simpan dinonaktifkan"*).
3. **Penyempurnaan Nilai Batas:**
   - *Tindakan Perbaikan:* Menambahkan skenario uji tiga titik nilai batas untuk pembayaran tunai (TC-09: pas batas Rp50.000, TC-10: di atas batas Rp60.000, dan TC-11: di bawah batas Rp40.000) untuk menjamin akurasi perhitungan laci kas kasir.

---

## 8. Matriks Keterlacakan Kebutuhan — Test Case (Langkah 9)

Matriks ini memetakan keterlacakan vertikal secara dua arah (*bidirectional traceability*) dari Spesifikasi Kebutuhan Fungsional (SRS), Use Case (UML), Rancangan Antarmuka (Wireframe), hingga Rencana Kasus Uji (Test Case).

**Kaidah Pemetaan:**
1. Semua kebutuhan prioritas *Must Have* dan *Should Have* wajib memiliki minimal satu *Test Case*.
2. Tidak boleh ada *Test Case* fiktif yang tidak berakar dari Kebutuhan Fungsional (KF).

| ID KF | Pernyataan Kebutuhan Fungsional | Use Case Terkait | Halaman Antarmuka (Wireframe) | Prioritas MoSCoW | ID Test Case |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **KF-01** | Menampilkan daftar menu dan kategori di layar POS | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-01` |
| **KF-02** | Tambah menu, ubah harga, dan ubah status menu (Tersedia/Habis) | `UC-05` (Kelola Menu) | `wf-04 Kelola Menu` | **Must** | `TC-02, TC-03, TC-04` |
| **KF-03** | Mencatat tipe pesanan Dine-in (No Meja) / Bungkus (Take-away) | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-05` |
| **KF-04** | Menghitung subtotal menu & total biaya pesanan otomatis | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-06, TC-07` |
| **KF-05** | Menolak penambahan menu berstatus habis ke keranjang pesanan | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-08` |
| **KF-06** | Menghitung nominal uang kembalian tunai secara otomatis | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-09, TC-10` |
| **KF-07** | Menolak transaksi tunai jika nominal uang bayar kurang | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-11` |
| **KF-08** | Menyediakan opsi metode bayar Tunai dan QRIS statis | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir` | **Must** | `TC-12` |
| **KF-09** | Menghasilkan nomor transaksi unik harian bertanggal | `UC-02` (Catat Penjualan) | `wf-02 POS Kasir`, `wf-03 Struk` | **Must** | `TC-13` |
| **KF-10** | Mencetak struk nota belanja dalam format thermal 58mm/80mm | `UC-04` (Cetak Struk) | `wf-03 Struk Pembayaran` | **Should** | `TC-14` |
| **KF-11** | Menampilkan riwayat transaksi penjualan hari berjalan | `UC-06` (Riwayat Transaksi) | `wf-05 Riwayat Transaksi` | **Should** | `TC-15` |
| **KF-12** | Rekapitulasi omzet harian memisahkan kas Tunai vs QRIS | `UC-07` (Laporan Omzet) | `wf-06 Laporan Omzet` | **Must** | `TC-16` |
| **KF-13** | Menampilkan 5 menu paling laris (*Top 5 Best Seller*) harian | `UC-07` (Laporan Omzet) | `wf-06 Laporan Omzet` | **Should** | `TC-17` |

### Rekapitulasi Cakupan Pengujian:
- **Total Kebutuhan Fungsional (Must & Should):** 13 butir (10 Must, 3 Should) $\rightarrow$ **Cakupan: 100% (13/13)**
- **Total Test Case yang Didefinisikan:** 17 kasus uji (termasuk 4 kasus tidak valid dan 3 pengujian nilai batas)
- **Status Keterlacakan:** Seluruh KF memiliki test case dan seluruh test case dapat dilacak kembali hingga ke kebutuhan awal pengguna.


