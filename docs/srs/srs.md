# SRS Ringkas — Sistem Kasir Warung Makan (KasirWarung)
## Software Requirements Specification (SRS)

---

### Informasi Dokumen
- **Nama Proyek:** Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*)
- **Mata Kuliah:** Rekayasa Perangkat Lunak (RPL)
- **Topik / Klien:** Usaha Kuliner Tradisional / Warung Makan UMKM
- **Versi:** v1.0 (*Baseline*)
- **Penyusun:** Tim RPL Mahasiswa D3 Teknologi Informasi
- **Tanggal:** November 2026

---

## 1. Pendahuluan

### 1.1 Tujuan dan Ruang Lingkup
Dokumen Spesifikasi Kebutuhan Perangkat Lunak (*Software Requirements Specification* - SRS) ini mendefinisikan seluruh kebutuhan fungsional dan non-fungsional yang wajib dipenuhi dalam pengembangan sistem kasir *Point of Sales* (POS) warung makan. 

Sistem ini dibangun untuk mengatasi kendala utama warung makan: kesalahan hitung manual dengan kalkulator di jam sibuk antrean makan siang, nota kertas yang rentan sobek/hilang, serta kesulitan pemilik merekapitulasi total uang tunai dan saldo QRIS di akhir hari. Ruang lingkup aplikasi mencakup operasional meja kasir (input pesanan, hitung total, hitung kembalian, cetak nota) dan modul manajerial pemilik warung (pengaturan menu/harga, status menu habis, dan rekapitulasi omzet harian) yang beroperasi secara andal di jaringan lokal (*offline-first*).

### 1.2 Definisi dan Istilah
- **POS (*Point of Sales*):** Titik penjualan atau perangkat lunak kasir tempat transaksi pembayaran diselesaikan.
- **Dine-in:** Layanan makan di tempat dengan mencantumkan nomor meja makan pelanggan.
- **Take-away / Bungkus:** Layanan pesanan makanan untuk dibawa pulang.
- **QRIS Statis:** Standar pembayaran kode QR nasional milik warung makan tanpa integrasi API perbankan otomatis. Kasir memverifikasi transaksi melalui bukti bayar di ponsel pembeli.
- **Printer Thermal:** Mesin pencetak struk mini berbasis kertas panas berukuran 58mm atau 80mm yang lazim digunakan pada meja kasir.
- **MoSCoW:** Metode penentuan prioritas kebutuhan (*Must have*, *Should have*, *Could have*, *Won't have*).

---

## 2. Gambaran Umum

### 2.1 Pengguna dan Peran
1. **Kasir / Pramusaji:** Bertugas melayani pembeli di meja kasir, memilih menu pesanan, menerima uang pembayaran, menginput nominal uang tunai, dan menyerahkan struk belanja. Karakteristik: memiliki literasi komputer dasar dan mengutamakan kecepatan interaksi antarmuka.
2. **Pemilik Warung (*Owner*):** Bertugas mengelola daftar menu lauk pauk, memperbarui harga jual, mengatur status ketersediaan (*Tersedia / Habis*), serta memantau ringkasan omzet harian untuk mencocokkan uang fisik di laci kasir saat tutup warung.

### 2.2 Lingkungan Operasi
- **Perangkat Keras (*Hardware*):** Dapat dijalankan pada PC Desktop, laptop kelas pemula (*entry-level*), maupun tablet kasir lokal dengan kapasitas RAM minimal 2 GB.
- **Sistem Operasi:** Kompatibel dengan Windows 10/11, Linux, maupun Android via peramban web modern (*Google Chrome, Microsoft Edge, Mozilla Firefox*).
- **Kondisi Jaringan & Listrik:** Beroperasi secara lokal (*localhost / intranet* warung). Sistem tidak mensyaratkan koneksi internet aktif agar kasir tetap dapat melayani transaksi saat jaringan internet publik sedang gangguan.

### 2.3 Batasan (*Constraints*)
1. **Waktu Pengerjaan:** Waktu pengembangan sistem dibatasi sampai Minggu 16 (terdiri dari empat siklus *Sprint* dua mingguan).
2. **Biaya & Anggaran:** Proyek dijalankan dengan anggaran nol rupiah untuk pihak ketiga; tidak menggunakan layanan basis data berbayar atau API *payment gateway* komersial yang mengenakan biaya per transaksi.
3. **Keterbatasan Pengguna:** Antarmuka harus menggunakan tombol berukuran besar (*touch-friendly*) dan teks berkontras tinggi agar dapat dioperasikan oleh kasir senior tanpa pelatihan rumit.

### 2.4 Asumsi dan Rencana Konfirmasi
1. **Asumsi 1:** Warung makan hanya menerima pembayaran Tunai dan transfer QRIS statis warung (tidak menggunakan mesin EDC kartu kredit/debit).  
   *Rencana Konfirmasi:* Divalidasi pada sesi wawancara langsung dengan pemilik warung makan.
2. **Asumsi 2:** Pencetakan struk dapat memanfaatkan dialog bawaan peramban (*browser print styling*) yang kompatibel dengan printer thermal standar 58mm melalui koneksi USB/Bluetooth.  
   *Rencana Konfirmasi:* Diuji langsung dengan printer kasir saat demonstrasi sistem.
3. **Asumsi 3:** Menu lauk pauk warung makan dimasak segar setiap hari, sehingga status menu *Tersedia* atau *Habis* diubah secara manual oleh kasir/pemilik saat lauk habis terjual.  
   *Rencana Konfirmasi:* Dikonfirmasi kepada pengelola warung terkait jadwal persiapan masakan harian.

---

## 3. Kebutuhan Fungsional (KF)

Sesuai kaidah baku RPL: setiap kebutuhan berupa kalimat berawalan *"Sistem harus ..."*, memiliki nomor unik, terukur, dan tidak menyebut teknologi perancangan.

| ID | Pernyataan Kebutuhan | Sumber | Prioritas | Asumsi? |
| :-: | :--- | :---: | :---: | :---: |
| **KF-01** | Sistem harus menampilkan daftar menu makanan dan minuman yang dikelompokkan berdasarkan kategori menu. | US-01 | **Must** | Tidak |
| **KF-02** | Sistem harus memungkinkan pemilik untuk menambah menu baru, mengubah harga jual, dan memperbarui status menu (Tersedia / Habis). | US-02 | **Must** | Tidak |
| **KF-03** | Sistem harus mencatat pilihan tipe pesanan pelanggan antara Makan di Tempat (Dine-in dengan nomor meja) atau Bungkus (Take-away). | US-03 | **Must** | Tidak |
| **KF-04** | Sistem harus menghitung subtotal tiap menu dan total keseluruhan biaya pesanan secara otomatis saat menu ditambahkan ke keranjang kasir. | US-04 | **Must** | Tidak |
| **KF-05** | Sistem harus menolak penambahan menu ke keranjang pesanan apabila status menu tersebut bertanda Habis dan menampilkan pesan peringatan. | US-05 | **Must** | Tidak |
| **KF-06** | Sistem harus menghitung nominal uang kembalian secara otomatis ketika kasir memasukkan jumlah uang tunai yang diserahkan pembeli. | US-06 | **Must** | Tidak |
| **KF-07** | Sistem harus menolak konfirmasi transaksi tunai jika nominal uang yang dimasukkan kasir kurang dari total tagihan belanja. | US-06 | **Must** | Tidak |
| **KF-08** | Sistem harus menyediakan pilihan metode pembayaran antara Tunai dan QRIS statis. | US-07 | **Must** | Tidak |
| **KF-09** | Sistem harus menghasilkan nomor transaksi unik dengan penanda tanggal dan nomor urut untuk setiap transaksi yang berhasil diselesaikan. | US-08 | **Must** | Tidak |
| **KF-10** | Sistem harus mencetak struk nota belanja transaksi dalam format struk thermal ringkas. | US-09 | **Should** | Tidak |
| **KF-11** | Sistem harus menampilkan riwayat transaksi penjualan yang terjadi pada hari berjalan beserta status pembayarannya. | US-10 | **Should** | Tidak |
| **KF-12** | Sistem harus menghasilkan rekapitulasi omzet harian yang memisahkan total penerimaan uang tunai fisik dan saldo masuk QRIS secara otomatis. | US-11 | **Must** | Tidak |
| **KF-13** | Sistem harus menampilkan ringkasan menu yang paling laris (*best seller*) berdasarkan jumlah porsi yang terjual pada tanggal berjalan. | US-12 | **Should** | Tidak |

### Alasan Prioritas MoSCoW:
- **Must Have (8 butir / 61.5%):** Butir KF-01 s.d. KF-09 dan KF-12 adalah fungsi inti kasir (*core POS*). Tanpa fungsi ini, sistem tidak dapat menggantikan peran kalkulator manual dan pencatatan kas harian warung makan.
- **Should Have (3 butir / 23%):** Butir KF-10 (Cetak Struk), KF-11 (Riwayat Transaksi), dan KF-13 (Menu Terlaris) sangat penting untuk kenyamanan pelanggan dan evaluasi pemilik, namun sistem penjualan inti masih dapat berjalan sementara meski struk kertas belum dicetak.

---

## 4. Kebutuhan Non-Fungsional (KNF)

Kebutuhan non-fungsional disusun dengan batasan dan ambang angka terukur:

| ID | Kategori | Pernyataan Terukur | Sumber |
| :-: | :--- | :--- | :---: |
| **KNF-01** | **Kinerja (*Performance*)** | Halaman utama antarmuka kasir harus dapat dimuat dan siap menerima input dalam waktu $\le 2\text{ detik}$ pada perangkat laptop klien. | Catatan Wawancara No. 4 |
| **KNF-02** | **Kinerja (*Performance*)** | Perhitungan subtotal dan total tagihan keranjang belanja harus selesai dalam waktu $\le 500\text{ milidetik}$ setelah menu dipilih. | Asumsi |
| **KNF-03** | **Keandalan (*Reliability*)** | Sistem harus dapat beroperasi penuh untuk transaksi penjualan secara lokal tanpa memerlukan koneksi internet (*offline-first*). | Catatan Wawancara No. 6 |
| **KNF-04** | **Kegunaan (*Usability*)** | Kasir baru yang belum pernah menggunakan komputer harus dapat menyelesaikan satu transaksi pesanan normal tanpa bantuan dalam waktu demonstrasi $\le 10\text{ menit}$. | Catatan Wawancara No. 7 |
| **KNF-05** | **Kegunaan (*Usability*)** | Ukuran teks utama nama menu, nominal total tagihan, dan uang kembalian pada layar kasir minimal berukuran 16 piksel dengan kontras visual tinggi agar terbaca jelas dari jarak $60\text{ cm}$. | Catatan Wawancara No. 7 |
| **KNF-06** | **Keamanan (*Security*)** | Sistem harus memvalidasi seluruh input nominal pembayaran dan harga di sisi pemrosesan server (*server-side validation*) untuk menolak nilai negatif atau teks non-angka. | Standar Keamanan RPL |

---

## 5. Di Luar Lingkup (*Won't Have* — Kali Ini)

Fitur berikut secara sadar **disepakati tidak dikerjakan** pada proyek ini untuk menjaga fokus dan mencegah pembengkakan ruang lingkup (*scope creep*):
1. **Pemindai Barcode (*Barcode Scanner*):** Masakan warung makan (lauk pauk, sayur mayur) disajikan di etalase/piring dan tidak memiliki kode batang pabrikan.
2. **Aplikasi Seluler Khusus (*Native Mobile App*):** Sistem berfokus pada aplikasi web responsif lokal di meja kasir.
3. **Payment Gateway Otomatis Dinamis:** Tidak menggunakan API pembayaran otomatis berbayar per transaksi; kasir cukup memverifikasi manual bukti transfer QRIS statis warung.
4. **Integrasi Layanan Ojek Online Luar:** Tidak terhubung dengan API pemesanan kurir GrabFood atau GoFood.

---

## 6. Matriks Keterlacakan (*Traceability Matrix*)

Memetakan hubungan dari kebutuhan awal (*User Story*) ke Kebutuhan Fungsional/Non-Fungsional (KF/KNF), serta rencana pengujian:

| User Story (US) | KF / KNF Turunan | Rencana Uji (*Test Case* - Minggu 13) |
| :--- | :--- | :--- |
| **US-01 (Katalog Menu)** | KF-01, KNF-01 | TC-01: Verifikasi pemuatan seluruh kategori dan menu di layar kasir $\le 2$ detik. |
| **US-02 (Kelola Menu & Harga)** | KF-02, KNF-06 | TC-02: Uji tambah menu, ubah harga, dan validasi input harga negatif ditolak. |
| **US-03 (Tipe Pesanan)** | KF-03 | TC-03: Uji pemilihan opsi Dine-in (No Meja) dan Bungkus pada struk pesanan. |
| **US-04 (Hitung Otomatis)** | KF-04, KNF-02 | TC-04: Uji akurasi matematis subtotal harga lauk + nasi $\times$ kuantitas. |
| **US-05 (Validasi Menu Habis)** | KF-05 | TC-05: Uji penolakan penambahan menu bertanda Habis ke keranjang pesanan. |
| **US-06 (Hitung Kembalian)** | KF-06, KF-07, KNF-06 | TC-06: Uji kalkulasi kembalian tunai dan verifikasi penolakan uang kurang. |
| **US-07 (Metode Bayar)** | KF-08 | TC-07: Uji pemilihan metode Tunai vs QRIS statis warung. |
| **US-08 (Nomor Transaksi)** | KF-09 | TC-08: Verifikasi keunikan nomor nota urut harian (`TRX-YYYYMMDD-XXX`). |
| **US-09 (Cetak Struk)** | KF-10, KNF-05 | TC-09: Uji tampilan cetak dialog peramban pas pada format thermal 58mm. |
| **US-10 (Riwayat Penjualan)** | KF-11 | TC-10: Verifikasi daftar seluruh transaksi tersimpan di database lokal. |
| **US-11 (Rekapitulasi Omzet)** | KF-12, KNF-03 | TC-11: Uji kesesuaian total omzet kotor, total Tunai, dan total QRIS saat tutup kasir. |
| **US-12 (Menu Terlaris)** | KF-13 | TC-12: Verifikasi urutan 5 menu dengan kuantitas porsi terjual terbanyak. |

---

## 7. Riwayat Konfirmasi Klien

| Tanggal | Narasumber / Klien | Ringkasan Tanggapan | Perubahan pada Kebutuhan |
| :---: | :--- | :--- | :--- |
| 11 Nov 2026 | Pemilik Warung Makan | Klien mengonfirmasi bahwa pembayaran terbanyak adalah Tunai dan sebagian pembeli muda memakai QRIS. Klien tidak membutuhkan mesin barcode. | Mempertahankan KF-08 (Tunai & QRIS), menegaskan scanner barcode masuk ke daftar *Won't Have*. |
| 11 Nov 2026 | Kasir Warung Makan | Meminta tombol menu berukuran besar dan perhitungan kembalian otomatis agar antrean jam makan siang tidak tersendat. | Menambahkan metrik terukur pada KNF-04 dan KNF-05 (font $\ge 16\text{ px}$). |
