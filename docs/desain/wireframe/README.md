# Dokumentasi Wireframe Antarmuka — Kasir Warung Makan (KasirWarung)
## Langkah 4 Sesi 1: Perancangan Antarmuka Sistem (Jobsheet 7)

Folder ini berisi seluruh artefak rancangan visual antarmuka kasar (*wireframe*) dan peta navigasi untuk **Sistem Kasir Warung Makan (*KasirWarung*)**. Seluruh rancangan dibuat dengan gaya monokrom (kotak dan garis) berfokus pada tata letak, alur interaksi, dan ruang pesan galat tanpa distraksi gaya visual akhir.

---

## 📋 Daftar Berkas Wireframe & Navigasi

| No | Berkas Gambar | Nama Halaman | Use Case Terkait | Keterangan Desain Kunci |
| :-: | :--- | :--- | :---: | :--- |
| 1 | [`navigasi.png`](navigasi.png) | **Peta Navigasi Aplikasi** | Seluruh UC | Alur perpindahan maksimal 2 klik antarhalaman dan pembagian hak akses peran. |
| 2 | [`wf-01-login.png`](wf-01-login.png) | **Halaman Login Petugas** | UC-01 | Kotak login terpusat, input username/password, dan pesan galat login gagal. |
| 3 | [`wf-02-pos-kasir.png`](wf-02-pos-kasir.png) | **Halaman Kasir / POS (Utama)** | UC-02, UC-03 | Grid tombol menu besar, pilihan Dine-in (No Meja) / Bungkus, keranjang belanja, kalkulasi otomatis, dan **peringatan menu habis**. |
| 4 | [`wf-03-struk.png`](wf-03-struk.png) | **Pratinjau Struk Pembayaran** | UC-04 | Format struk thermal mini 58mm/80mm, rincian nota, tombol cetak, dan tombol pesanan baru. |
| 5 | [`wf-04-kelola-menu.png`](wf-04-kelola-menu.png) | **Manajemen Menu & Harga (Pemilik)** | UC-05 | Tabel data menu, filter kategori, tombol tambah menu, dan toggle status *Tersedia / Habis*. |
| 6 | [`wf-05-riwayat.png`](wf-05-riwayat.png) | **Riwayat Transaksi Penjualan** | UC-06 | Tabel riwayat transaksi hari ini, filter tanggal/metode, dan tombol lihat rincian nota. |
| 7 | [`wf-06-laporan-omzet.png`](wf-06-laporan-omzet.png) | **Laporan Rekapitulasi Omzet (Pemilik)** | UC-07 | 4 kartu ringkasan (Omzet, Tunai, QRIS, Total Nota) dan tabel 5 Menu Paling Laris (*Top 5*). |

---

## 🔍 Penjelasan Komponen Standar pada Setiap Wireframe
Sesuai arahan Langkah 4 Jobsheet 7, setiap wireframe memuat:
1. **Judul Halaman:** Ditampilkan jelas di bagian atas konten.
2. **Menu Navigasi Konsisten:** Bilah navigasi atas (*top navbar*) yang seragam di seluruh halaman.
3. **Area Isi:** Formulir isian, grid menu tombol, atau tabel data.
4. **Tombol Aksi:** Tombol dengan kontras tegas di posisi yang mudah dijangkau.
5. **Ruang Pesan Umpan Balik / Galat:** Kotak bergaris putus-putus (*dashed border*) untuk peringatan gagal atau pesan sukses.
