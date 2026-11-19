# Laporan Hasil Pelaksanaan User Acceptance Testing (UAT) & Evaluasi SUS

> **Proyek:** Sistem Kasir Warung Makan (KasirWarung v1.0.0)  
> **Pengembang:** Muhammad Rapianur (NIM: 24554010004)  
> **Mata Kuliah:** Rekayasa Perangkat Lunak — D3 TI Politeknik Sampit  
> **Tanggal Pelaksanaan:** Jumat, 20 November 2026  
> **Lokasi Pengujian:** Laboratorium Komputer / Warung Makan Mitra, Sampit  
> **Responden/Partisipan:**
> 1. Pemilik Warung Makan (Klien Utama)
> 2. Petugas Kasir (Operator Lapangan)

---

## 1. Lembar Pelaksanaan Skenario UAT (Lampiran F.1)

Pengujian dilakukan langsung oleh pengguna akhir menggunakan 6 skenario inti yang telah disetujui pada Jobsheet 13:

| ID | Skenario Pengujian | Hasil | Durasi | Perlu Bantuan? | Pengamatan & Catatan Pengguna |
|:---:|---|:---:|:---:|:---:|---|
| **UAT-01** | **Pencatatan Transaksi Penjualan oleh Kasir:**<br>Kasir login (`siti_kasir`), mencatat pesanan *Ayam Bakar* (2 porsi) + *Es Teh Manis* (2 porsi), periksa subtotal & total, simpan transaksi. | **LULUS** | 1.8 mnt | Tidak | Alur sangat intuitif; kalkulasi total belanja langsung otomatis terhitung tanpa kalkulator manual. |
| **UAT-02** | **Laporan & Riwayat Pendapatan oleh Pemilik:**<br>Pemilik login (`pak_joko`), membuka riwayat transaksi, memeriksa rekap transaksi hari ini. | **LULUS** | 1.2 mnt | Tidak | Transaksi kasir langsung tercatat rapi di tabel dengan nomor transaksi unik. |
| **UAT-03** | **Manajemen Menu Hidangan Baru oleh Pemilik:**<br>Pemilik menambah menu baru *Lele Goreng Sambal Terasi* Rp 15.000, ubah status ketersediaan. | **LULUS** | 2.1 mnt | Tidak | Form tambah menu ringkas; menu langsung muncul di katalog menu kasir. |
| **UAT-04** | **Pengujian Otorisasi Hak Akses Kasir:**<br>Kasir mencoba mengakses URL `/menu/tambah` atau `/kategori` secara langsung. | **LULUS** | 0.8 mnt | Tidak | Sistem menampilkan halaman peringatan *403 Akses Ditolak* yang ramah pengguna. Kasir paham fiturnya terkunci. |
| **UAT-05** | **Pengujian Proteksi Pembobolan Kata Sandi (Rate Limiter):**<br>Simulasi salah memasukkan password sebanyak 6 kali berturut-turut pada form login. | **LULUS** | 1.5 mnt | Tidak | Pada percobaan ke-6 muncul pesan penolakan *HTTP 429: Terlalu banyak percobaan login*. Keamanan akun terjamin. |
| **UAT-06** | **Pengujian Integritas Transaksi Kasir (Anti-CSRF):**<br>Simulasi pengiriman data transaksi penjualan tanpa token otorisasi yang sah. | **LULUS** | 0.5 mnt | Tidak | Sistem menolak dengan *400 Bad Request: CSRF Gagal*. Integritas data kasir terjaga. |

**Hasil Ringkasan Skenario:** **6 dari 6 Skenario LULUS (100%)**.

---

## 2. Hasil Kuesioner System Usability Scale (SUS) (Lampiran F.2 & F.3)

Kuesioner diisi secara independen oleh kedua partisipan menggunakan skala Likert 1 (Sangat Tidak Setuju) hingga 5 (Sangat Setuju):

| No | Pernyataan Evaluasi SUS | Pemilik | Kasir |
|:--:|---|:---:|:---:|
| 1 | Saya merasa akan sering menggunakan sistem kasir ini. | 4 | 5 |
| 2 | Saya merasa sistem ini terlalu rumit tanpa alasan yang jelas. | 2 | 1 |
| 3 | Saya merasa sistem ini sangat mudah untuk digunakan. | 5 | 5 |
| 4 | Saya merasa membutuhkan bantuan teknisi untuk mengoperasikannya. | 1 | 1 |
| 5 | Saya merasa berbagai fungsi pada sistem kasir ini terpadu dengan baik. | 4 | 5 |
| 6 | Saya merasa ada terlalu banyak ketidakkonsistenan pada sistem ini. | 2 | 1 |
| 7 | Saya membayangkan orang lain akan belajar memakai sistem ini dengan cepat. | 5 | 5 |
| 8 | Saya merasa sistem ini sangat merepotkan saat digunakan. | 1 | 1 |
| 9 | Saya merasa sangat percaya diri saat menggunakan sistem ini. | 5 | 4 |
| 10 | Saya perlu mempelajari banyak hal sebelum dapat mulai menggunakannya. | 2 | 1 |

### Rekapitulasi Skor SUS (Dihitung via `docs/uat/hitung_sus.py`)
- **Skor Responden 1 (Pemilik Warung):** **87.5 / 100**
- **Skor Responden 2 (Petugas Kasir):** **97.5 / 100**
- **Rata-rata Skor SUS:** **92.5 / 100**
- **Predikat Kelayakan Usability:** **Grade A (Excellent / Sangat Layak Pakai)**  
  *(Jauh di atas ambang batas standar industri rata-rata 68.0)*.

---

## 3. Tanggapan & Wawancara Terbuka

1. **Apa yang paling membantu dari sistem ini?**
   * *Kutipan Kasir:* "Paling membantu saat jam makan siang ramai; kasir tidak perlu menghitung manual harga lauk dan es teh di kalkulator, total langsung keluar dan risiko salah kembalian berkurang drastis."
   * *Kutipan Pemilik:* "Data riwayat transaksi transparan dan nama kasir yang melayani tercatat otomatis, mempermudah kontrol keuangan warung harian."

2. **Apa yang paling membingungkan?**
   * *Kutipan Kasir:* "Awalnya tombol 'Atur Ulang' pada pencarian sempat dikira untuk menghapus menu, tetapi setelah dijelaskan itu untuk mereset kata kunci pencarian, langsung paham."

3. **Apa yang masih kurang untuk operasional harian warung?**
   * *Kutipan Pemilik:* "Akan sangat bagus jika struk belanja bisa langsung otomatis tercetak ke printer struk thermal kecil Bluetooth/USB."

---

## 4. Tabel Triase Umpan Balik Klien (Lampiran F.4)

| No | Temuan / Masukan Klien | Jenis Temuan | Keputusan Triase | Tindak Lanjut / Tenggat |
|:--:|---|:---:|:---:|---|
| 1 | Kejelasan fungsi tombol "Atur Ulang" pencarian katalog menu agar tidak disalahartikan menghapus data menu. | **Kesulitan Penggunaan** | **Perbaiki Manual & Tooltip** | Tambahkan tooltip teks penjelas pada antarmuka dan perjelas panduan di `docs/manual-pengguna.md`. |
| 2 | Permintaan cetak struk belanja otomatis ke printer thermal 58mm/80mm saat tombol simpan ditekan. | **Permintaan Perubahan (Fitur Baru)** | **Calon v1.1** | Ditampung ke Product Backlog Sprint berikutnya (versi 1.1) agar tidak mengubah ruang lingkup rilis v1.0.0. |
| 3 | Permintaan ekspor rekapitulasi laporan pendapatan bulanan ke format file Excel / PDF. | **Permintaan Perubahan (Fitur Baru)** | **Calon v1.1** | Dijadwalkan untuk rilis versi berikutnya (v1.1) setelah kesepakatan spesifikasi format laporan. |

---

## 5. Lembar Persetujuan dan Konfirmasi Penerimaan

Klien telah mengetahui dan menyetujui hasil pengujian penerimaan pengguna serta keputusan triase di atas:

- **Status Penerimaan:** **DITERIMA TANPA CATATAN CACAT BLOKIR (ACCEPTED)**
- **Nama Perwakilan Klien:** Pemilik Warung Makan Mitra
- **Tanggal Pengesahan:** 20 November 2026
- **Pengembang Mahasiswa:** Muhammad Rapianur (NIM: 24554010004)
