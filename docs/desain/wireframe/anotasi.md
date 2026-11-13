# Anotasi Antarmuka dan Penerapan Prinsip Desain — KasirWarung
## Langkah 5 Sesi 1: Perancangan Antarmuka Sistem (Jobsheet 7)

Dokumen ini memuat tabel anotasi elemen bernomor pada wireframe antarmuka kasir warung makan, pemetaan terhadap 5 prinsip dasar heuristik antarmuka (Nielsen), serta evaluasi perbaikan sebelum–sesudah rancangan.

---

## 1. Tabel Anotasi Halaman Utama POS Kasir (`wf-02-pos-kasir.png`)

Nomor merujuk pada penanda lingkaran (*callout badge*) pada berkas gambar [`wf-02-pos-kasir.png`](wf-02-pos-kasir.png):

| No | Elemen Antarmuka | Data / Aksi | Aturan / Pesan yang Muncul | Prinsip Desain (Bagian 2.3) |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Bilah Navigasi Atas (*Top Navbar*)** | Menampilkan menu: *POS Kasir*, *Riwayat*, *Kelola Menu (Pemilik)*, *Laporan Omzet (Pemilik)*, serta identitas kasir aktif. | • Letak dan format teks seragam di seluruh halaman aplikasi.<br>• Menu manajerial disembunyikan jika login sebagai kasir biasa. | **Konsistensi** & **Kesederhanaan** |
| **2** | **Pemilihan Tipe Pesanan & No Meja** | Dropdown pilihan: *Makan di Tempat (Dine-in)* atau *Bungkus (Take-away)* beserta input nomor meja. | • Jika memilih *Makan di Tempat*, input nomor meja wajib diisi.<br>• Jika memilih *Bungkus*, input nomor meja otomatis dinonaktifkan (*disabled*) dan bernilai `NULL`. | **Pencegahan Galat (*Error Prevention*)** |
| **3** | **Kotak Peringatan Galat / Pengecualian** | Kotak peringatan garis putus-putus (*dashed border*) warna merah muda. | • Muncul seketika jika kasir menekan menu berstatus *Habis*:<br>*"Peringatan: Menu Ayam Bakar sedang HABIS dan tidak dapat ditambahkan!"*<br>• Muncul jika uang bayar kurang:<br>*"Nominal uang bayar kurang dari total belanja!"* | **Umpan Balik (*Feedback*)** |
| **4** | **Grid Tombol Menu Touch-Friendly** | Tombol-tombol kartu menu makanan/minuman berukuran besar dengan nama menu dan harga jelas. | • Font nama menu dan harga berukuran $\ge 16\text{ px}$ dengan kontras visual tinggi (KNF-05).<br>• Menu berstatus *Habis* otomatis berwarna abu-abu redup (*disabled*) dengan label tegas `[HABIS]` agar kasir tidak salah tekan. | **Keterbacaan** & **Pencegahan Galat** |
| **5** | **Panel Pembayaran & Tombol Simpan Nota** | Input uang tunai yang diterima, pilihan radio button *Tunai / QRIS*, kalkulasi kembalian otomatis, dan tombol aksi *Bayar & Simpan*. | • Tombol *Bayar & Simpan* terletak konsisten di pojok kanan bawah.<br>• Tombol tidak dapat diklik (*disabled*) jika keranjang masih kosong atau nominal uang tunai kurang dari total belanja. | **Konsistensi** & **Pencegahan Galat** |

---

## 2. Tabel Anotasi Halaman Pendukung

### A. Halaman Login (`wf-01-login.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Kotak Peringatan Login | Pesan kegagalan autentikasi | Muncul jika password salah: *"Galat: Nama pengguna atau kata sandi tidak valid."* | **Umpan Balik** |
| **2** | Isian Username | Input teks nama akun | Wajib diisi, tidak boleh spasi, autofocus saat halaman dimuat. | **Pencegahan Galat** |
| **3** | Isian Password | Input teks bertopeng (`type="password"`) | Karakter kata sandi disembunyikan demi keamanan privasi di meja kasir. | **Keamanan** |
| **4** | Tombol Masuk | Aksi login ke sistem | Memvalidasi kredensial ke database SQLite dan mengarahkan sesuai peran. | **Umpan Balik** |

### B. Halaman Struk Nota Pembayaran (`wf-03-struk.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Baris Notifikasi Berhasil | Banner hijau status pembayaran | *"Transaksi Berhasil Disimpan (Lunas)"* memberi kepastian transaksi sukses tercatat di SQLite. | **Umpan Balik** |
| **2** | Format Struk Mini 58mm | Tampilan monokrom nota thermal | Menampilkan nama warung, nomor nota unik, tanggal, rincian lauk, total, dan kembalian. Font monospaced. | **Keterbacaan** |
| **3** | Tombol Cetak Thermal | Aksi cetak ke printer kasir | Memicu dialog cetak peramban dengan format CSS `@media print` 58mm/80mm. | **Konsistensi** |
| **4** | Tombol Pesanan Baru | Aksi reset antarmuka kasir | Mengosongkan keranjang dan kembali ke halaman POS kasir untuk melayani antrean berikutnya. | **Kesederhanaan** |

### C. Halaman Kelola Menu (`wf-04-kelola-menu.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Penanda Hak Akses Navbar | Indikator menu navigasi aktif | Hanya dapat dilihat dan diakses oleh akun dengan peran Pemilik. | **Konsistensi** |
| **2** | Tombol Tambah Menu | Membuka modal form menu baru | Menampilkan form isian nama menu, kategori, harga ($\ge 0$), dan status. | **Kesederhanaan** |
| **3** | Banner Notifikasi Pembaruan | Umpan balik aksi status | *"Status menu Ayam Bakar berhasil diubah menjadi: HABIS."* | **Umpan Balik** |
| **4** | Toggle Status Ketersediaan | Tombol switch Tersedia / Habis | Mengubah status menu secara instan tanpa perlu reload halaman penuh. | **Pencegahan Galat** |
| **5** | Tombol Aksi Ubah / Hapus | Modifikasi master menu | Tombol hapus memicu dialog konfirmasi: *"Yakin ingin menghapus menu ini?"* | **Pencegahan Galat** |

### D. Halaman Laporan Omzet (`wf-06-laporan-omzet.png`)
| No | Elemen | Data / Aksi | Aturan / Pesan | Prinsip |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Indikator Peran Pemilik | Menu navbar aktif | Menu Laporan hanya tampil bagi pemilik warung makan. | **Konsistensi** |
| **2** | Filter Rentang Tanggal | Input tanggal mulai & selesai | Standar ISO `YYYY-MM-DD`, membatasi tanggal selesai tidak boleh lebih awal dari tanggal mulai. | **Pencegahan Galat** |
| **3** | Kartu Metrik Kas (Cards) | 4 indikator ringkasan omzet | Menampilkan Total Omzet, Kas Tunai Fisik (cocok dengan laci kas), Saldo QRIS, dan Total Nota. Angka berukuran besar. | **Keterbacaan** |
| **4** | Tabel 5 Menu Terlaris | Peringkat menu terlaris | Mengagregasi jumlah porsi terjual dari `detail_transaksi` secara otomatis. | **Umpan Balik** |

---

## 3. Catatan Evaluasi Sebelum–Sesudah Penerapan Prinsip

Berikut adalah 3 contoh perbaikan konkret yang dilakukan pada antarmuka berdasarkan evaluasi 5 prinsip heuristik:

### Contoh 1: Penanganan Menu Habis pada Halaman POS Kasir
- **Sebelum Evaluasi (Rancangan Awal):**
  Semua tombol menu memiliki warna dan bentuk yang sama persis. Kasir dapat mengklik menu yang stoknya sudah habis di etalase, lalu sistem baru memunculkan pesan error saat tombol bayar ditekan di akhir alur. Ini membuang waktu dan membingungkan kasir saat jam sibuk.
- **Sesudah Evaluasi (Penerapan Prinsip *Pencegahan Galat* & *Keterbacaan*):**
  Menu yang berstatus *Habis* langsung ditampilkan dengan gaya visual khusus: latar belakang abu-abu pudar, garis tepi putus-putus, label merah tebal `[HABIS]`, dan tombol dibuat tidak dapat diklik (*disabled*). Kesalahan dicegah sejak awal sebelum pesanan masuk ke keranjang.

### Contoh 2: Kalkulasi Kembalian Uang Tunai
- **Sebelum Evaluasi:**
  Kasir harus menghitung uang kembalian secara manual di kepala atau kalkulator eksternal, lalu mengetikkan nominal kembalian ke form. Hal ini rawan salah hitung (*human error*).
- **Sesudah Evaluasi (Penerapan Prinsip *Pencegahan Galat* & *Umpan Balik*):**
  Kasir cukup mengetikkan nominal uang kertas yang diserahkan pelanggan pada kotak *Uang Diterima*. Sistem secara otomatis menghitung selisih dan menampilkan angka kembalian berwarna hijau terang dengan ukuran font 16 piksel. Tombol simpan otomatis dinonaktifkan jika uang yang diserahkan kurang dari total tagihan.

### Contoh 3: Navigasi Menu Pemilik vs Kasir
- **Sebelum Evaluasi:**
  Seluruh menu (*Kelola Menu* dan *Laporan Omzet*) terpampang di navbar kasir sehingga petugas kasir sering tidak sengaja membuka halaman laporan keuangan pemilik.
- **Sesudah Evaluasi (Penerapan Prinsip *Kesederhanaan* & *Konsistensi*):**
  Menu di navbar disesuaikan secara dinamis berdasarkan hak akses peran: akun Kasir hanya melihat *POS Kasir* dan *Riwayat Transaksi*, sedangkan akun Pemilik memiliki akses lengkap. Halaman kasir tetap bersih dan fokus pada tugas pelayanan transaksi.
