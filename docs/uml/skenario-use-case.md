# Skenario Use Case — Sistem Kasir Warung Makan

Dokumen ini memuat rincian perilaku dan skenario untuk setiap *use case* pada sistem kasir warung makan, disusun berdasarkan format baku Lampiran B Jobsheet 5 mata kuliah Rekayasa Perangkat Lunak.

---

## Tabel Pemetaan Use Case ke Kebutuhan Fungsional (KF)

| ID Use Case | Nama Use Case | Aktor Utama | Kebutuhan Terkait (PRD/SRS) | Prioritas |
| :---: | :--- | :--- | :--- | :---: |
| **UC-01** | Login Sistem | Kasir, Pemilik | FR-01, NFR-Security | Must |
| **UC-02** | Mencatat Transaksi Penjualan | Kasir | FR-03, FR-04, FR-05, FR-06, FR-07, FR-12 | Must |
| **UC-03** | Cek Ketersediaan Menu | Kasir (Include oleh UC-02) | FR-01, FR-02 | Must |
| **UC-04** | Mencetak Struk Pembayaran | Kasir (Extend terhadap UC-02) | FR-08 | Must |
| **UC-05** | Mengelola Data Menu | Pemilik | FR-01, FR-02 | Must |
| **UC-06** | Melihat Riwayat Transaksi | Kasir, Pemilik | FR-09 | Should |
| **UC-07** | Melihat Rekapitulasi Omzet | Pemilik | FR-10, FR-11 | Must |

---

## 1. UC-01: Login Sistem

- **Aktor:** Kasir, Pemilik
- **KF Terkait:** FR-01, NFR-Security
- **Prasyarat:** Pengguna berada pada halaman login aplikasi web kasir.

### Alur Utama
1. Pengguna membuka peramban web dan mengakses tautan sistem kasir.
2. Sistem menampilkan formulir login yang memuat kolom username dan password.
3. Pengguna memasukkan username serta password, lalu menekan tombol "Masuk".
4. Sistem memverifikasi kecocokan kredensial pengguna ke basis data lokal.
5. Sistem menentukan hak akses pengguna (peran Kasir diarahkan ke halaman antarmuka kasir/POS; peran Pemilik diarahkan ke ringkasan menu & laporan).
6. Sistem menampilkan pesan selamat datang dan antarmuka sesuai peran.

### Alur Alternatif
- **3a. Pengguna sudah memiliki sesi aktif (session cookie valid):**
  - Sistem langsung mengarahkan pengguna ke halaman utama peran tanpa meminta input password kembali.

### Pengecualian
- **4a. Kredensial tidak cocok (username salah atau password keliru):**
  - Sistem menolak proses autentikasi dan menampilkan pesan peringatan: *"Nama pengguna atau kata sandi tidak valid. Silakan coba kembali."*
  - Kolom input password dikosongkan dan kursor kembali aktif di kolom input username.

### Pascakondisi
- Sesi pengguna tercatat aktif dan pengguna dapat mengakses modul fungsional sesuai hak aksesnya.

---

## 2. UC-02: Mencatat Transaksi Penjualan

- **Aktor:** Kasir
- **KF Terkait:** FR-03, FR-04, FR-05, FR-06, FR-07, FR-12
- **Prasyarat:** Kasir telah berhasil login dan membuka halaman antarmuka kasir (*Point of Sales*).

### Alur Utama
1. Kasir memilih jenis pesanan: "Makan di Tempat (Dine-in)" dengan memilih nomor meja atau "Bungkus (Take-away)".
2. Kasir memilih menu makanan/minuman dari grid tombol menu yang ditampilkan.
3. Sistem secara otomatis memicu proses *Cek Ketersediaan Menu* (UC-03).
4. Menu yang dipilih ditambahkan ke dalam daftar keranjang pesanan.
5. Sistem mengalikan kuantitas (*qty*) dengan harga satuan, kemudian memperbarui subtotal dan total harga transaksi secara *real-time*.
6. Kasir menekan tombol "Proses Pembayaran".
7. Kasir memilih metode pembayaran "Tunai" dan menginput jumlah uang tunai yang diserahkan pelanggan.
8. Sistem menghitung nominal uang kembalian secara otomatis.
9. Kasir menekan tombol "Konfirmasi & Simpan Transaksi".
10. Sistem menyimpan data transaksi ke basis data, menghasilkan nomor transaksi unik, dan mengosongkan keranjang pesanan untuk pesanan berikutnya.

### Alur Alternatif
- **2a. Kasir mengubah jumlah pesanan (*qty*) atau menghapus menu:**
  - Kasir menekan tombol minus/hapus pada keranjang pesanan, sistem langsung menghitung ulang total harga.
- **7a. Pelanggan memilih metode pembayaran "QRIS":**
  - Kasir memilih opsi bayar "QRIS", sistem menampilkan kode QR statis warung di layar.
  - Setelah pelanggan menunjukkan bukti transfer berhasil, kasir mencentang "Pembayaran Terverifikasi" dan langsung memproses transaksi tanpa perlu hitung kembalian.

### Pengecualian
- **3a. Menu yang dipilih berstatus "Habis":**
  - Sistem menolak penambahan menu ke keranjang dan menampilkan pesan peringatan: *"Menu [Nama Menu] sedang habis dan tidak dapat dipesan."*
- **8a. Nominal uang tunai yang diinput kurang dari total belanja:**
  - Sistem menampilkan peringatan berwarna merah: *"Nominal uang bayar kurang dari total tagihan!"* dan menonaktifkan tombol simpan transaksi sampai uang yang diinput bernilai $\ge \text{total tagihan}$.
- **9a. Keranjang pesanan masih kosong saat tombol pembayaran ditekan:**
  - Sistem menampilkan notifikasi: *"Keranjang pesanan masih kosong. Pilih minimal satu menu."*

### Pascakondisi
- Transaksi baru tercatat di database dengan status lunas. Keranjang belanja bersih dan siap untuk antrean pelanggan berikutnya.

---

## 3. UC-03: Cek Ketersediaan Menu

- **Aktor:** Kasir (dipanggil secara otomatis oleh UC-02 via relasi `<<include>>`)
- **KF Terkait:** FR-01, FR-02
- **Prasyarat:** Sistem menerima input permintaan penambahan item menu ke keranjang pesanan kasir.

### Alur Utama
1. Sistem menerima kode/ID menu yang diklik oleh kasir.
2. Sistem memeriksa atribut status ketersediaan menu di database lokal (`status = 'tersedia'`).
3. Sistem mengonfirmasi bahwa menu berstatus aktif dan mengizinkan item masuk ke keranjang belanja.

### Alur Alternatif
- Tidak ada alur alternatif; use case ini merupakan fungsi validasi tunggal yang dipanggil sistem.

### Pengecualian
- **2a. Status menu di basis data bernilai 'habis':**
  - Sistem memblokir aksi penambahan item, memberi tanda visual abu-abu (*disabled*) pada tombol menu tersebut di UI, dan memunculkan pesan peringatan ketiadaan stok.

### Pascakondisi
- Status item tervalidasi dengan aman sebelum tagihan diakumulasikan.

---

## 4. UC-04: Mencetak Struk Pembayaran

- **Aktor:** Kasir (berelasi `<<extend>>` terhadap UC-02)
- **KF Terkait:** FR-08
- **Prasyarat:** Transaksi penjualan (UC-02) telah selesai diproses dan disimpan ke sistem.

### Alur Utama
1. Sistem menampilkan halaman rangkuman transaksi sukses beserta pratinjau struk ringkas digital.
2. Kasir menekan tombol "Cetak Struk".
3. Sistem memicu jendela dialog cetak peramban (*browser print dialog*) dengan format stylesheet khusus thermal 58mm/80mm.
4. Kasir menekan "Print" untuk mengirimkan data ke printer thermal kasir.
5. Printer mencetak bukti nota transaksi yang memuat nama warung, tanggal, nomor transaksi, rincian pesanan, total bayar, dan nominal kembalian.

### Alur Alternatif
- **1a. Pelanggan tidak memerlukan struk fisik:**
  - Kasir tidak menekan tombol cetak, melainkan langsung menekan tombol "Pesanan Baru" untuk kembali ke antarmuka POS tanpa mencetak kertas struk (perilaku *extend* opsional).

### Pengecualian
- **3a. Printer thermal tidak terhubung atau kertas habis:**
  - Sistem dialog peramban mendeteksi status printer tidak siap, kasir dapat membatalkan dialog cetak tanpa membatalkan transaksi yang telah tersimpan di database.

### Pascakondisi
- Lembar struk fisik berhasil dicetak atau dilewati sesuai permintaan pelanggan.

---

## 5. UC-05: Mengelola Data Menu

- **Aktor:** Pemilik
- **KF Terkait:** FR-01, FR-02
- **Prasyarat:** Pemilik telah login dan membuka halaman "Manajemen Menu".

### Alur Utama
1. Pemilik membuka menu navigasi "Kelola Menu".
2. Sistem menampilkan tabel daftar seluruh menu makanan dan minuman (nama menu, kategori, harga satuan, dan status).
3. Pemilik menekan tombol "Tambah Menu Baru".
4. Pemilik mengisi formulir data menu: nama menu, pilihan kategori (Makanan/Minuman/Lauk/Ekstra), harga jual, dan status ketersediaan.
5. Pemilik menekan tombol "Simpan Menu".
6. Sistem memvalidasi kelengkapan isian formulir.
7. Sistem menyimpan data menu baru ke basis data dan menampilkan pesan sukses: *"Menu berhasil ditambahkan."*
8. Daftar tabel menu otomatis diperbarui dengan data menu terbaru.

### Alur Alternatif
- **3a. Pemilik ingin mengubah harga atau mengganti status menu menjadi 'Habis':**
  - Pemilik memilih tombol "Ubah / Edit" pada baris menu yang diinginkan.
  - Pemilik mengganti harga atau mengubah status toggle ketersediaan, lalu menekan tombol "Perbarui".
  - Sistem menyimpan perubahan dan memperbarui status menu secara instan di layar kasir.

### Pengecualian
- **6a. Kolom harga diisi nilai kosong, teks bukan angka, atau angka negatif:**
  - Sistem menolak penyimpanan dan menampilkan pesan validasi: *"Harga menu harus berupa angka positif."*
- **6b. Nama menu sudah terdaftar sebelumnya dalam kategori yang sama:**
  - Sistem menampilkan peringatan: *"Nama menu sudah ada dalam sistem. Gunakan nama yang berbeda atau ubah menu yang ada."*

### Pascakondisi
- Master data menu makanan/minuman berhasil diperbarui dan langsung tercermin di antarmuka kasir.

---

## 6. UC-07: Melihat Rekapitulasi Omzet

- **Aktor:** Pemilik
- **KF Terkait:** FR-10, FR-11
- **Prasyarat:** Pemilik telah login dan memilih menu "Laporan Penjualan".

### Alur Utama
1. Pemilik membuka halaman "Laporan Penjualan & Omzet".
2. Sistem menampilkan ringkasan penjualan harian tanggal berjalan yang mencakup:
   - Total pendapatan kotor (*Gross Revenue*).
   - Rincian penerimaan: Total Uang Tunai fisik vs Total Masuk via QRIS.
   - Total frekuensi transaksi yang berhasil diselesaikan hari ini.
   - Tabel daftar menu terlaris (*Top 5 Best Seller*) beserta jumlah porsi yang laku.
3. Pemilik meninjau data rekapitulasi untuk pencocokan fisik uang laci (*cash drawer*).

### Alur Alternatif
- **2a. Pemilik ingin melihat rekapitulasi pada rentang tanggal tertentu:**
  - Pemilik mengisi filter rentang tanggal (tanggal awal s.d. tanggal akhir) lalu menekan tombol "Tampilkan".
  - Sistem menghitung ulang akumulasi transaksi sesuai rentang tanggal tersebut.

### Pengecualian
- **2b. Belum ada transaksi yang terjadi pada tanggal yang dipilih:**
  - Sistem menampilkan kartu informasi: *"Belum ada data transaksi penjualan pada tanggal ini (Omzet: Rp0)."*

### Pascakondisi
- Pemilik memperoleh data ringkasan omzet yang valid dan siap digunakan untuk evaluasi kas harian warung.
