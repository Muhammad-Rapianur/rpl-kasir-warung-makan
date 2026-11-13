# Lembar Tinjauan Design Review (Langkah 11)
### Lampiran C — Evaluasi Rancangan Antarmuka & Pengujian

---

**Informasi Peninjauan:**
- **Kelompok Penelaah:** Kelompok 2 (Sistem Inventaris Bahan Baku)
- **Kelompok yang Ditinjau / Proyek:** Kelompok 1 — Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*)
- **Tanggal Peninjauan:** 14 November 2026
- **Metode Tinjauan:** *Peer Review* Antarkelompok (Presentasi Draf & Walkthrough Repositori)

---

## 1. Daftar Periksa Antarmuka dan Pengujian

| No | Pertanyaan Periksa | Ya | Tidak | Catatan / Ulasan Penelaah |
| :-: | :--- | :---: | :---: | :--- |
| **1** | Setiap use case Must dapat diselesaikan melalui halaman yang digambar? | **[v]** | [ ] | Seluruh use case Must (katalog menu, pencatatan transaksi, kelola menu, dan laporan omzet) terakomodasi di `wf-02`, `wf-04`, dan `wf-06`. |
| **2** | Peta navigasi jelas; setiap halaman dapat dicapai dan ada jalan kembali? | **[v]** | [ ] | Peta navigasi visual (`navigasi.mmd`) sangat terstruktur dengan pemisahan peran Kasir dan Pemilik, serta setiap halaman memiliki tombol kembali/keluar. |
| **3** | Menu, tombol, dan istilah konsisten di semua halaman? | **[v]** | [ ] | Tata letak bilah navigasi atas konsisten dengan warna monokrom dan hierarki tipografi rapi. |
| **4** | Pesan keberhasilan dan galat tergambar (umpan balik)? | **[v]** | [ ] | Banner peringatan menu habis dan validasi uang bayar kurang tergambar eksplisit di `wf-02`. |
| **5** | Isian dibatasi untuk mencegah galat (angka, wajib isi)? | **[v]** | [ ] | Dropdown kategori dan input angka harga dibatasi dengan batasan validasi angka positif. |
| **6** | Tulisan terbaca dan memakai istilah klien? | **[v]** | [ ] | Menggunakan istilah yang akrab bagi warung lokal: *Dine-in (Meja)*, *Bungkus*, *Lauk & Sayur*, serta nominal Rupiah yang jelas. |
| **7** | Setiap KF Must punya test case; hasil diharapkan terukur? | **[v]** | [ ] | Terdapat 17 test case dengan hasil terukur eksplisit, termasuk 4 kasus tidak valid dan 3 nilai batas untuk uang pembayaran. |
| **8** | Ada elemen yang tidak berasal dari SRS (fitur tambahan)? | [ ] | **[v]** | Tidak ada fitur fiktif seperti mesin barcode atau e-wallet dinamis yang menyimpang dari SRS. |

---

## 2. Kekuatan Rancangan (≥ 1)
1. **Ergonomi Layar Kasir Sangat Cepat:** Desain pembagian 2 kolom pada `wf-02` (katalog tombol menu di kiri dan keranjang ringkasan di kanan) memungkinkan kasir menginput pesanan dan menyelesaikan transaksi dalam hitungan detik tanpa berpindah halaman.
2. **Detail Pratinjau Struk Thermal:** Wireframe `wf-03` secara realistis mendesain layout kertas struk 58mm dengan tipografi monospace, batas pemisah strip (`---`), dan rincian kasir/meja yang pas untuk printer kasir warung makan.
3. **Penyusunan Rencana Uji Sangat Matang:** Matriks keterlacakan 100% lengkap menghubungkan KF, Use Case, Halaman Wireframe, hingga ID Test Case konkret (`TC-01` s.d. `TC-17`).

---

## 3. Temuan Penting (Menghalangi Use Case) & Usulan
1. **Temuan 1 — Tombol Pintasan Uang Pas / Uang Pecahan Cepat:**
   - *Kondisi:* Pada `wf-02 POS Kasir`, kasir harus mengetikkan nominal uang tunai secara manual di kolom input teks (misal: mengetik `50000`).
   - *Alasan Masalah:* Saat antrean jam makan siang sangat ramai, mengetik angka nominal di keyboard laptop memperlambat transaksi kasir dan rawan salah ketik digit nol (misal: kurang nol menjadi `5000` atau lebih nol menjadi `500000`).
   - *Usulan:* Sediakan tombol bantuan nominal cepat (*quick cash pills*), misalnya tombol instan `[Uang Pas]`, `[Rp20.000]`, `[Rp50.000]`, `[Rp100.000]` di samping kolom input uang tunai.
2. **Temuan 2 — Tombol Cetak Ulang pada Riwayat Transaksi:**
   - *Kondisi:* Pada `wf-05 Riwayat Transaksi`, kasir/pemilik hanya dapat melihat daftar tabel tanpa adanya aksi cetak ulang struk.
   - *Alasan Masalah:* Jika kertas printer thermal macet (*paper jam*) atau habis saat transaksi diselesaikan, kasir memerlukan cara untuk mencetak ulang (*re-print*) nota dari riwayat transaksi tanpa harus mengulang pesanan dari awal.
   - *Usulan:* Tambahkan tombol aksi `[Cetak Ulang Struk]` pada setiap baris riwayat transaksi di `wf-05`.

---

## 4. Saran Perbaikan (Opsional)
1. **Indikator Koneksi Offline / Jaringan Lokal:**
   - *Alasan:* Mengingat sistem mengusung konsep *offline-first*, akan lebih menenangkan bagi kasir jika terdapat badge kecil di bilah atas antarmuka bertuliskan `[● Mode Offline Lokal - Siap Melayani]`.

---

## 5. Pertanyaan untuk Kelompok
1. *"Jika ada pembeli yang memesan 'Dine-in' (Makan di Tempat) kemudian di tengah makan menambah es teh manis, bagaimana alur pencatatannya di kasir? Apakah membuat nota baru atau mengedit nota meja tersebut?"*
