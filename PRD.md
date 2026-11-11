# Product Requirements Document (PRD)
## Sistem Kasir Warung Makan (KasirWarung)

---

### Informasi Dokumen
- **Nama Proyek:** Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*)
- **Mata Kuliah:** Rekayasa Perangkat Lunak (RPL)
- **Topik / Tema:** Aplikasi Kasir Point of Sales (POS) UMKM Kuliner Tradisional / Warung Makan
- **Versi Dokumen:** v1.0
- **Status:** *Approved / Baseline*
- **Target Platform:** Web Application (Responsive Desktop / Tablet / Smartphone Lokal)
- **Tanggal Penyusunan:** November 2026

---

## 1. Latar Belakang & Identifikasi Masalah

### 1.1 Konteks Lapangan
Warung makan merupakan salah satu model UMKM kuliner yang memiliki perputaran transaksi harian sangat cepat, khususnya pada jam-jam sibuk (makan siang dan makan malam). Sebagian besar warung makan tradisional masih mengandalkan pencatatan pesanan dan perhitungan total belanja secara manual menggunakan kertas nota, coretan tangan, atau ingatan kasir semata.

### 1.2 Masalah Utama (*Problem Statements*)
1. **Risiko Salah Hitung (*Human Error*):** Perhitungan manual saat suasana ramai sering menyebabkan kesalahan total harga makanan, terutama pada pesanan dengan banyak menu sampingan/lauk tambahan, yang berujung pada kerugian pemilik atau keluhan dari pelanggan.
2. **Antrean Pembayaran Menumpuk:** Kasir membutuhkan waktu lama untuk mengingat harga tiap lauk, menjumlahkan dengan kalkulator, dan menghitung uang kembalian, sehingga memperlambat alur antrean kasir.
3. **Pencatatan Penjualan Tidak Terarsip Rapi:** Kertas nota pesanan rentan sobek, basah terkena kuah/minyak, atau hilang. Akibatnya, pemilik kesulitan merekap berapa porsi makanan yang terjual pada hari itu.
4. **Ketidaksesuaian Kas (*Cash Discrepancy*):** Di akhir jam buka, pemilik sering menemukan ketidakcocokan antara uang fisik di laci kasir dengan estimasi penjualan makanan, ditambah kesulitan memisahkan pembayaran tunai (*cash*) dan nontunai (QRIS statis).
5. **Kesulitan Menentukan Porsi Stok Harian:** Tanpa data riwayat menu terlaris, pemilik sering mengalami kelebihan persediaan lauk basah (yang berisiko basi/rugi) atau kekurangan lauk yang banyak dicari pelanggan.

---

## 2. Visi Produk & Tujuan (*Goals & Objectives*)

### 2.1 Visi Produk
Menghadirkan aplikasi kasir (*Point of Sale*) warung makan yang ringan, cepat, minim klik (*low friction*), ramah pengguna (*low learning curve*), dan dapat beroperasi andal secara lokal (*local network/offline-first*) untuk membantu warung makan mengelola transaksi, cetak nota, serta rekap pendapatan secara akurat tanpa biaya operasional yang memberatkan.

### 2.2 Tujuan Proyek (*Objectives*)
1. **Mempercepat Pelayanan Kasir:** Mengurangi rata-rata waktu proses transaksi pembayaran dari >60 detik (manual) menjadi <15 detik per transaksi.
2. **Menjamin Akurasi Finansial 100%:** Mengotomatiskan perhitungan subtotal, diskon (jika ada), total bayar, dan nominal kembalian uang pelanggan.
3. **Rekapitulasi Otomatis:** Menghasilkan laporan penjualan harian dan rincian metode pembayaran (Tunai vs QRIS) secara otomatis dalam satu klik saat tutup toko.
4. **Pengelolaan Menu Dinamis:** Memberikan kemudahan bagi pengelola untuk memperbarui menu, harga lauk, dan status ketersediaan lauk (*Tersedia / Habis*).

### 2.3 Metrik Keberhasilan (*Key Performance Indicators / KPIs*)
- **Efisiensi Waktu Transaksi:** Waktu penyelesaian transaksi di kasir <= 15 detik.
- **Akurasi Hitung Kas:** 0% selisih perhitungan matematis antara rincian transaksi dengan nota.
- **Tingkat Kemudahan Pakai (*Usability*):** Kasir atau pramusaji dapat mengoperasikan alur pesanan dasar dengan waktu pelatihan kurang dari 15 menit.
- **Keringanan Sistem (*Performance*):** Waktu respons pemuatan halaman kasir < 1 detik pada jaringan lokal dengan perangkat laptop kelas *entry-level*.

---

## 3. Profil Pengguna & Persona (*Target Audience*)

| Persona | Peran | Tugas Utama | Kebutuhan Utama |
| :--- | :--- | :--- | :--- |
| **Kasir / Pramusaji** | Operasional | Melayani pesanan pembeli, input menu, terima pembayaran, serahkan struk. | Tampilan kasir dengan tombol menu visual yang besar, kalkulasi kembalian otomatis, tombol cepat cetak/simpan struk, minim langkah klik. |
| **Pemilik Warung (*Owner*)** | Manajerial & Supervisi | Menentukan daftar menu & harga, memantau omzet harian, mengecek rekap kas saat tutup warung. | Akses ke laporan harian, rekapitulasi total uang tunai vs saldo masuk QRIS, ringkasan menu paling laris (*best seller*). |

---

## 4. Ruang Lingkup Produk (*Product Scope*)

### 4.1 Dalam Ruang Lingkup (*In-Scope / MVP*)
1. **Modul Manajemen Menu & Kategori:**
   - Pengelompokan kategori: Makanan Utama, Sayur/Lauk Pauk, Minuman, dan Ekstra/Camilan (kerupuk, sambal, gorengan).
   - Pengaturan harga jual per porsi/item.
   - Penandaan status menu: *Tersedia* / *Habis*.
2. **Modul Kasir (*Point of Sales - POS*):**
   - Tampilan antarmuka kasir berbasis grid menu visual yang mudah ditekan (*touch-friendly*).
   - Pemilihan jenis pesanan: *Makan di Tempat (Dine-in)* dengan nomor meja atau *Bungkus/Bawa Pulang (Take-away)*.
   - Keranjang pesanan dinamis (*cart*): penambahan jumlah (*qty*), pembatalan item, dan catatan pesanan (misal: "tidak pakai pedas").
   - Kalkulasi otomatis subtotal, total harga, input nominal uang dibayar, dan nominal kembalian.
   - Pilihan metode pembayaran: **Tunai** dan **QRIS** (tampilan kode QR statis warung).
3. **Modul Struk & Nota Pembelian:**
   - Pembuatan nomor transaksi unik berbasis tanggal & urutan (contoh: `TRX-20261111-001`).
   - Format tampilan struk ringkas yang siap dicetak ke printer thermal 58mm/80mm atau dicetak via dialog print browser.
4. **Modul Riwayat & Rekapitulasi Harian:**
   - Tabel riwayat transaksi hari berjalan.
   - Ringkasan total pemasukan harian, rincian per metode bayar (Tunai vs QRIS), dan total transaksi yang berhasil diselesaikan.
   - Ringkasan jumlah porsi menu yang laku terjual hari ini.

### 4.2 Di Luar Ruang Lingkup (*Out-of-Scope / Non-Goal*)
- **Bukan Sistem E-Commerce / Delivery Online:** Tidak menyediakan fitur pemesanan jarak jauh oleh konsumen melalui kurir ojek online (Grab/Gojek API).
- **Tanpa Pemindai Barcode:** Makanan warung makan tidak memakai kode batang pabrikan.
- **Tanpa Payment Gateway Otomatis Dinamis:** Tidak memerlukan integrasi webhook payment gateway perbankan berbayar (cukup verifikasi manual bukti pembayaran QRIS statis warung).
- **Tanpa Akuntansi Korporasi Rumit:** Tidak mencakup pembukuan jurnal ganda, faktur pajak PPN 11%, atau modul penggajian karyawan multi-cabang.

---

## 5. Kebutuhan Fungsional (*Functional Requirements*)

| Kode FR | Modul | Deskripsi Kebutuhan | Aktor | Prioritas (MoSCoW) |
| :---: | :--- | :--- | :---: | :---: |
| **FR-01** | Menu | Kasir/Pemilik dapat melihat seluruh daftar menu makanan dan minuman terkelompok berdasarkan kategori. | Kasir, Pemilik | **Must Have** |
| **FR-02** | Menu | Pemilik dapat menambah, mengubah, dan menonaktifkan status menu (*Tersedia / Habis*). | Pemilik | **Must Have** |
| **FR-03** | Kasir | Kasir dapat memilih jenis pesanan (*Makan di Tempat* + No Meja, atau *Bungkus*). | Kasir | **Must Have** |
| **FR-04** | Kasir | Kasir dapat menambahkan menu ke keranjang pesanan dengan satu kali klik/tap dan mengatur kuantitas (*qty*). | Kasir | **Must Have** |
| **FR-05** | Kasir | Sistem menghitung subtotal tiap menu dan total keseluruhan tagihan secara otomatis *real-time*. | Sistem | **Must Have** |
| **FR-06** | Kasir | Sistem menghitung jumlah uang kembalian secara otomatis saat kasir menginput jumlah uang yang diterima dari pelanggan. | Kasir, Sistem | **Must Have** |
| **FR-07** | Kasir | Kasir dapat memilih metode pembayaran antara Tunai atau QRIS. | Kasir | **Must Have** |
| **FR-08** | Struk | Sistem menghasilkan struk digital setelah transaksi selesai dan menyediakan tombol cetak format thermal. | Kasir, Sistem | **Must Have** |
| **FR-09** | Riwayat | Kasir dan Pemilik dapat melihat riwayat transaksi yang terjadi pada hari berjalan beserta status pembayarannya. | Kasir, Pemilik | **Should Have** |
| **FR-10** | Rekap | Pemilik dapat melihat ringkasan omzet harian: total pendapatan kotor, pembagian nominal Tunai vs QRIS, serta jumlah transaksi. | Pemilik | **Must Have** |
| **FR-11** | Rekap | Pemilik dapat melihat urutan menu terlaris (*top selling items*) pada periode hari berjalan. | Pemilik | **Should Have** |
| **FR-12** | Kasir | Kasir dapat membatalkan atau mereset keranjang belanja sebelum transaksi disimpan ke sistem. | Kasir | **Must Have** |

---

## 6. Kebutuhan Non-Fungsional (*Non-Functional Requirements*)

### 6.1 Performa (*Performance*)
- Waktu respons perpindahan halaman atau penambahan item ke keranjang kasir tidak melebihi **500 milidetik**.
- Proses penyimpanan transaksi dan pembuatan struk selesai dalam waktu kurang dari **2 detik**.

### 6.2 Kemudahan Penggunaan (*Usability*)
- Antarmuka kasir dirancang dengan tombol berukuran memadai (*touch-friendly*) agar nyaman dioperasikan pada tablet layar sentuh atau laptop kasir.
- Tipografi teks harga, nama menu, dan nominal kembalian menggunakan kontras tinggi dan ukuran font yang mudah dibaca oleh petugas kasir dari jarak pandang normal.

### 6.3 Keandalan & Lingkungan Kerja (*Reliability & Environment*)
- Sistem dirancang untuk mampu berjalan pada server lokal (*localhost / intranet offline*) di dalam warung makan, sehingga operasional kasir tetap berjalan lancar meski koneksi internet luar sedang mengalami gangguan.
- Data transaksi tersimpan persisten ke dalam basis data relasional lokal (SQLite) yang aman dan ringan tanpa dependensi layanan berbayar.

### 6.4 Keamanan & Validasi (*Security & Data Integrity*)
- Seluruh input kasir (harga, jumlah uang diterima, kuantitas) divalidasi ketat di sisi server (*server-side validation*) untuk mencegah angka negatif, pembagian nol, atau data tidak valid.
- Bebas dari kerentanan web mendasar seperti *Cross-Site Scripting* (XSS) dan *SQL Injection* dengan menggunakan mekanisme templating aman Jinja2 dan query berparameter / ORM.

---

## 7. Arsitektur Sistem & Spesifikasi Teknologi

- **Bahasa Pemrograman:** Python (versi 3.10+)
- **Framework Web:** Flask (ringan, modular, mudah disesuaikan dengan kebutuhan lokal)
- **Mesin Templating:** Jinja2 + HTML5 / CSS3 Modern (responsif, desain bersih tanpa *bloatware*)
- **Basis Data:** SQLite (berkas lokal `kasir_warung.db`, tanpa perlu setup server database terpisah yang berat)
- **Arsitektur:** Model-View-Controller (MVC) terstruktur sederhana
- **Integrasi Hardware Kasir:** Dukungan dialog cetak browser langsung (*browser print styling* `@media print`) yang kompatibel dengan printer thermal USB/Bluetooth 58mm & 80mm.

---

## 8. Aturan Proyek (*Project Guidelines & Standards*)

Seluruh pengembangan proyek **Sistem Kasir Warung Makan** dalam lingkup tugas mata kuliah Rekayasa Perangkat Lunak (RPL) wajib mematuhi aturan berikut:

### 8.1 Prinsip Rekayasa Kebutuhan & Vibe Coding
1. **Berpijak pada Realitas Lapangan (*Grounded Requirements*):** Kebutuhan dan fitur yang dikembangkan harus merefleksikan alur kerja nyata warung makan. Dilarang keras menambahkan fitur fiktif/halusinasi seperti pemindai barcode, integrasi e-commerce global, atau kecerdasan buatan rumit yang tidak dibutuhkan oleh warung makan.
2. **Kritik & Validasi Luaran AI (*Human-in-the-Loop*):** Kode atau rancangan yang dihasilkan oleh asisten AI wajib diuji fungsinya secara mandiri, ditinjau keamanannya, dan divalidasi kesesuaian logikanya sebelum diterima (*Accept / Reject / Modify*).
3. **Privasi & Etika Data:** Segala data riil narasumber pemilik warung (nama lengkap, kontak pribadi, data omzet riil sensitif) wajib disamarkan atau dianonimkan dalam dokumentasi publik dan repositori.

### 8.2 Konvensi Repositori & Kontrol Versi (Git)
1. **Branching Strategy:**
   - `main`: Branch produksi yang berisi kode stabil dan siap didemokan.
   - `feature/<nama-fitur>`: Branch kerja untuk setiap modul/fitur baru (misal: `feature/pos-cart`, `feature/cetak-struk`, `feature/rekap-omzet`).
2. **Format Pesan Commit (*Conventional Commits*):**
   - `feat: <penjelasan>` untuk penambahan fitur baru.
   - `fix: <penjelasan>` untuk perbaikan bug/kesalahan logika.
   - `docs: <penjelasan>` untuk pembaruan dokumentasi (PRD, user story, pedoman wawancara).
   - `style: <penjelasan>` untuk perapian tampilan CSS tanpa mengubah fungsi.
   - `refactor: <penjelasan>` untuk restrukturisasi kode tanpa mengubah fungsionalitas.
3. **Sanitasi Repositori:**
   - Direktori lingkungan virtual (`.venv/`), berkas cache (`__pycache__/`), dan berkas konfigurasi lokal tidak boleh di-commit ke Git (wajib masuk `.gitignore`).

### 8.3 Standar Koding & Struktur Berkas
- Struktur folder repositori harus teratur dan modular:
  ```text
  rpl-kasir-warung-makan/
  ├── docs/
  │   ├── elisitasi/            <-- Hasil elisitasi: pedoman, catatan wawancara, user story
  │   │   ├── catatan-wawancara.md
  │   │   ├── pedoman-wawancara.md
  │   │   └── user-story.md
  │   ├── uml/                  <-- Khusus diagram perancangan UML (Use Case, Activity, Class)
  │   ├── PRD.md                <-- Dokumen Kebutuhan Produk (PRD)
  │   └── aturan-proyek.md      <-- Aturan tata kelola proyek
  ├── static/
  │   ├── css/
  │   └── js/
  ├── templates/
  │   ├── kasir.html
  │   ├── menu.html
  │   ├── struk.html
  │   └── laporan.html
  ├── .gitignore
  ├── app.py
  ├── aturan-proyek.md
  ├── PRD.md
  ├── README.md
  └── requirements.txt
  ```
- Variabel dan fungsi Python menggunakan format `snake_case`.
- Nama templat dan berkas dokumen menggunakan huruf kecil dan tanda hubung (`kebab-case`).

### 8.4 Definisi Selesai (*Definition of Done - DoD*)
Sebuah modul atau fitur dinyatakan selesai apabila:
1. Memenuhi seluruh kriteria penerimaan fungsional (*Given-When-Then*) yang telah disepakati pada *User Story*.
2. Lolos pengujian manual pada alur normal (*happy path*) dan alur perkecualian (*edge cases*, seperti input uang kurang atau kuantitas nol).
3. Tampilan responsif dan tidak merusak tata letak visual di resolusi layar standar (laptop dan tablet).
4. Kode telah ditinjau, bebas error sintaksis, dan berhasil di-commit dengan pesan commit berstandar.
5. Log keputusan dicatat secara transparan pada jurnal proyek.