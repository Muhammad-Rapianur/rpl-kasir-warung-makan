# Keputusan Revisi Rancangan Pasca-Design Review (Langkah 12)

Dokumen ini mencatat tindak lanjut dan keputusan tim pengembang KasirWarung terhadap hasil masukan rekan penelaah pada Lembar Tinjauan (*Peer Design Review*).

---

## 1. Tabel Keputusan Masukan Penelaah

| No | Masukan Penelaah | Keputusan | Perubahan / Alasan Justifikasi |
| :-: | :--- | :---: | :--- |
| **1** | **Penambahan Tombol Nominal Uang Pecahan Cepat (*Quick Cash Buttons*):**<br>Sediakan tombol instan `[Uang Pas]`, `[Rp20.000]`, `[Rp50.000]`, `[Rp100.000]` di samping input uang tunai kasir (`wf-02`). | **TERIMA** | **Perubahan:** Rancangan antarmuka POS kasir ditambahkan deretan tombol pill nominal cepat di bawah input uang tunai. Hal ini secara signifikan memangkas waktu input kasir pada jam sibuk dan mencegah salah ketik digit nol (*zero-typing error*). |
| **2** | **Aksi Cetak Ulang Struk (*Reprint*) pada Riwayat Transaksi:**<br>Tambahkan tombol aksi `[Cetak Ulang]` pada setiap baris riwayat nota di halaman Riwayat Transaksi (`wf-05`). | **TERIMA** | **Perubahan:** Menambahkan tombol ikon cetak pada kolom 'Aksi' di tabel `wf-05 Riwayat Transaksi` yang mengarahkan kasir langsung ke dialog cetak `wf-03 Struk`. Hal ini mengatasi risiko operasional bila kertas printer thermal macet (*paper jam*). |
| **3** | **Alur Tambah Pesanan Susulan (*Add-on Order*) untuk Pelanggan Dine-in:**<br>Klarifikasi bagaimana sistem menangani pelanggan yang menambah pesanan saat sedang makan di meja. | **TANYA KLIEN** | **Alasan:** Pada kesepakatan awal wawancara, sistem dirancang untuk pembayaran di awal saat pesan (*pay-at-the-counter*). Jika klien menghendaki sistem *pay-at-the-end* (bayar belakangan setelah selesai makan), maka diperlukan fitur *Hold Order / Open Bill*. Tim memutuskan mengonfirmasikan hal ini langsung ke pemilik warung tanpa terburu-buru merombak arsitektur basis data. |
| **4** | **Penyatuan Pembayaran Split (Sebagian Tunai + Sebagian QRIS):**<br>Usulan dari penelaah untuk mengizinkan satu transaksi dibayar 50% tunai dan 50% QRIS. | **TOLAK** | **Alasan:** Ditolak karena pada *Jobsheet 6 Langkah 14*, pemilik warung telah secara tegas mengonfirmasi bahwa metode pembayaran wajib satu jenis (Tunai murni atau QRIS murni) demi menjaga kesederhanaan rekapitulasi kasir dan integritas skema DDL `CHECK (metode_pembayaran IN ('tunai', 'qris'))`. |
| **5** | **Badge Status Koneksi Offline:**<br>Menampilkan indikator visual mode offline-first di header navigasi. | **TERIMA** | **Perubahan:** Menambahkan elemen status visual hijau `[● Mode Offline Lokal]` pada bilah navigasi utama untuk meningkatkan ketenangan dan kepercayaan diri kasir saat koneksi internet padam. |

---

## 2. Dampak Revisi terhadap Dokumen dan Artefak
1. **Dampak pada Wireframe:**
   - `docs/desain/wireframe/wf-02-pos-kasir.html`: Ditambahkan tombol pill `[Uang Pas]`, `[20k]`, `[50k]`, `[100k]`.
   - `docs/desain/wireframe/wf-05-riwayat.html`: Ditambahkan tombol `[Cetak Ulang]` pada kolom Aksi tabel.
2. **Dampak pada Rencana Pengujian:**
   - Ditambahkan skenario uji verifikasi tombol nominal cepat pada pengujian fungsional kasir.
3. **Dampak pada Basis Data & Arsitektur:**
   - Tidak ada perubahan struktural pada skema tabel SQLite (`schema.sql`), integritas skema 3NF tetap terjaga kokoh.

---

## 3. Catatan Jurnal Vibe Coding (Pelajaran dari Design Review)
> **Pelajaran Penting (Insight):**  
> *"Menerima evaluasi dari pihak luar (kelompok sejawat) memberikan sudut pandang operasional yang sering luput dari pengembang internal. Kasus kegagalan fisik (seperti kertas printer thermal macet atau kepanikan kasir mengetik digit nol di jam sibuk) membuktikan bahwa desain antarmuka perangkat lunak tidak hanya harus benar secara kode, namun harus ramah dan tahan banting terhadap dinamika kerja nyata di lapangan."*
