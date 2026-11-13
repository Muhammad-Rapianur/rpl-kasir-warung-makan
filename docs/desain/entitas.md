# Identifikasi Entitas Sistem — Kasir Warung Makan (KasirWarung)
## Langkah 2 Sesi 1: Perancangan Basis Data (Jobsheet 6)

Dokumen ini memuat hasil penelusuran dan penentuan entitas basis data untuk **Sistem Kasir Warung Makan (*KasirWarung*)** berdasarkan dokumen spesifikasi kebutuhan ([SRS Ringkas](../srs/srs.md)), [PRD.md](../../PRD.md), dan skenario use case ([skenario-use-case.md](../uml/skenario-use-case.md)).

---

## 1. Analisis Kata Benda & Seleksi Entitas

Setiap kandidat kata benda diuji dengan dua pertanyaan penyaring sesuai pedoman Jobsheet 6:
1. *Apakah sistem perlu mengingat dan menyimpannya ke dalam basis data?*
2. *Apakah ia memiliki banyak contoh data (banyak baris/rekaman)?*

| Kata Benda Kandidat | Perlu Disimpan? | Banyak Baris? | Status | Alasan / Keputusan |
| :--- | :---: | :---: | :---: | :--- |
| **Pengguna / Kasir / Pemilik** | Ya | Ya | **Entitas (`pengguna`)** | Memiliki akun kasir dan pemilik untuk login serta melacak siapa yang mencatat transaksi. |
| **Kategori Menu** | Ya | Ya | **Entitas (`kategori`)** | Mengelompokkan menu (Makanan, Minuman, Lauk, Ekstra) agar tampilan kasir teratur. |
| **Menu Makanan / Minuman** | Ya | Ya | **Entitas (`menu`)** | Memiliki banyak item lauk/minuman, harga satuan, dan status ketersediaan harian. |
| **Transaksi / Nota Penjualan** | Ya | Ya | **Entitas (`transaksi`)** | Setiap pembayaran pelanggan menghasilkan rekaman penjualan unik yang wajib disimpan. |
| **Rincian Pesanan Menu** | Ya | Ya | **Entitas (`detail_transaksi`)** | Memecah relasi banyak-ke-banyak antara Transaksi dan Menu (menyimpan kuantitas & harga saat beli). |
| *Laporan / Rekap Omzet* | Tidak | Tidak | **Bukan Entitas** | Laporan adalah hasil olahan kueri agregasi (`SUM`, `COUNT`) dari tabel transaksi, bukan tabel tersimpan. |
| *Struk Pembayaran* | Tidak | Tidak | **Bukan Entitas** | Struk adalah tampilan visual/cetak (*view*) dari gabungan data transaksi dan detail transaksi. |
| *Keranjang Belanja (Cart)* | Tidak | Tidak | **Bukan Entitas** | Data sementara (*in-memory / session*) di antarmuka kasir sebelum tombol simpan ditekan. |
| *Uang Kembalian* | Tidak | Tidak | **Bukan Entitas** | Nilai kalkulasi matematis turunan (`uang_diterima - total_tagihan`). |

---

## 2. Tabel Entitas Terpilih (Sesuai Format Langkah 2 Jobsheet 6)

| No | Entitas (Tabel) | Deskripsi | Sumber Kebutuhan (KF / UC) |
| :-: | :--- | :--- | :--- |
| **1** | **`pengguna`** | Menyimpan data akun kasir dan pemilik warung makan untuk otentikasi login, pembedaan hak akses, dan pelacakan kasir yang bertugas melayani transaksi. | **UC-01** (Login Sistem), **NFR-06** (Keamanan Akun) |
| **2** | **`kategori`** | Menyimpan data klasifikasi jenis menu (Makanan Utama, Sayur/Lauk Pauk, Minuman, Ekstra/Camilan) untuk pengorganisasian grid menu di antarmuka kasir. | **KF-01** (Katalog Menu Berdasarkan Kategori), **UC-05** (Kelola Menu) |
| **3** | **`menu`** | Menyimpan master data makanan dan minuman yang dijual warung makan beserta harga satuan dan status ketersediaan harian (*Tersedia / Habis*). | **KF-01**, **KF-02**, **KF-05**, **UC-02**, **UC-03**, **UC-05** |
| **4** | **`transaksi`** | Menyimpan data kepala (*header*) transaksi penjualan (nomor transaksi unik, waktu transaksi, jenis pesanan Dine-in/Bungkus, nomor meja, metode bayar Tunai/QRIS, nominal uang diterima, dan kasir yang memproses). | **KF-03**, **KF-06**, **KF-07**, **KF-08**, **KF-09**, **KF-11**, **KF-12**, **UC-02**, **UC-06**, **UC-07** |
| **5** | **`detail_transaksi`** | Tabel penghubung (*junction table*) antara `transaksi` dan `menu` yang mencatat rincian porsi menu yang dipesan, kuantitas (*qty*), harga satuan saat transaksi, dan catatan khusus pesanan. | **KF-04** (Kalkulasi Item), **KF-09** (Penyimpanan Transaksi), **KF-13** (Menu Terlaris), **UC-02** |

---

## 3. Kesimpulan & Verifikasi Batasan
- Jumlah entitas terpilih: **5 entitas** (memenuhi batas panduan Jobsheet 6: rentang 4–8 entitas).
- Seluruh entitas tertelusur (*traceable*) ke Kebutuhan Fungsional (KF) di SRS dan Skenario Use Case.
- Tidak ada entitas "fitur" atau olahan tampilan semu (seperti laporan atau struk).
