# Daftar Halaman Antarmuka — Kasir Warung Makan (KasirWarung)
## Langkah 2 Sesi 1: Penurunan Halaman dari Use Case (Jobsheet 7)

Dokumen ini memuat daftar halaman aplikasi web yang diturunkan secara langsung dari skenario *use case* ([`docs/uml/skenario-use-case.md`](../uml/skenario-use-case.md)) dan kamus data ([`docs/desain/kamus-data.md`](../desain/kamus-data.md)) untuk **Sistem Kasir Warung Makan (*KasirWarung*)**.

---

## Tabel Penurunan Halaman dari Use Case (Format Langkah 2 Jobsheet 7)

| No | Kode / Nama Halaman | Use Case yang Dilayani | Aktor yang Berhak Mengakses | Data yang Ditampilkan / Diproses (Merujuk Kamus Data) |
| :-: | :--- | :---: | :---: | :--- |
| **1** | **`wf-01` : Halaman Login** | **UC-01** (Login Sistem) | Kasir, Pemilik | `pengguna.username`, `pengguna.password_hash` (input), pesan galat login. |
| **2** | **`wf-02` : Halaman POS Kasir (Catat Penjualan)** | **UC-02** (Catat Penjualan),<br>**UC-03** (Cek Menu) | Kasir, Pemilik | `kategori.nama`, `menu.nama`, `menu.harga`, `menu.status`, `transaksi.tipe_pesanan`, `transaksi.nomor_meja`, `detail_transaksi.jumlah`, `detail_transaksi.harga_satuan`, subtotal, total (kalkulasi `SUM`), `transaksi.metode_pembayaran`, `transaksi.uang_diterima`, uang kembalian, pesan galat (*menu habis / uang kurang*). |
| **3** | **`wf-03` : Halaman / Dialog Struk Pembayaran** | **UC-04** (Cetak Struk) | Kasir | `transaksi.nomor_transaksi`, `transaksi.tanggal_waktu`, `pengguna.nama_lengkap`, `transaksi.tipe_pesanan`, `transaksi.nomor_meja`, rincian `menu.nama`, `detail_transaksi.jumlah`, `detail_transaksi.harga_satuan`, `detail_transaksi.catatan`, total bayar, `transaksi.metode_pembayaran`, `transaksi.uang_diterima`, kembalian. |
| **4** | **`wf-04` : Halaman Manajemen Menu & Harga** | **UC-05** (Kelola Data Menu) | Pemilik | `menu.id`, `kategori.nama`, `menu.nama`, `menu.harga`, `menu.status` (toggle *Tersedia / Habis*), form modal tambah/ubah menu, pesan validasi. |
| **5** | **`wf-05` : Halaman Riwayat Transaksi** | **UC-06** (Lihat Riwayat Transaksi) | Kasir, Pemilik | `transaksi.nomor_transaksi`, `transaksi.tanggal_waktu`, `pengguna.nama_lengkap`, `transaksi.tipe_pesanan`, `transaksi.metode_pembayaran`, total bayar, tombol lihat rincian nota & cetak ulang. |
| **6** | **`wf-06` : Halaman Rekapitulasi Omzet & Laporan** | **UC-07** (Lihat Rekapitulasi Omzet) | Pemilik | Filter tanggal, total akumulasi omzet kotor, total kas Tunai fisik, total saldo QRIS, jumlah transaksi selesai, tabel peringkat 5 menu terlaris (`menu.nama`, total porsi terjual). |

---

## Verifikasi Keterpenuhan Syarat Langkah 2:
1. **Jumlah Halaman:** Tepat **6 halaman** (memenuhi syarat minimal 6 halaman).
2. **Cakupan Use Case:** Seluruh *use case* berkategori **Must** (`UC-01`, `UC-02`, `UC-03`, `UC-04`, `UC-05`, `UC-07`) dan **Should** (`UC-06`) tercakup lengkap.
3. **Kesesuaian Kamus Data:** Seluruh kolom data merujuk secara konsisten pada tabel `pengguna`, `kategori`, `menu`, `transaksi`, dan `detail_transaksi`.
4. **Pembedaan Hak Akses:** Halaman manajerial (Kelola Menu dan Rekap Omzet) hanya dapat dibuka oleh aktor **Pemilik**, sedangkan alur operasional kasir dapat diakses oleh **Kasir** dan Pemilik.
