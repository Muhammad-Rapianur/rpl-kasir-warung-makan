# Atribut, Kunci, dan Batasan Sistem — Kasir Warung Makan (KasirWarung)
## Langkah 3 Sesi 1: Perancangan Basis Data (Jobsheet 6)

Dokumen ini memuat perincian atribut, kunci utama (*Primary Key*), kunci unik (*Unique Key*), kunci asing (*Foreign Key*), serta batasan integritas data (*constraints*) untuk setiap entitas pada **Sistem Kasir Warung Makan (*KasirWarung*)**.

---

## 1. Tabel Atribut dan Batasan (Sesuai Format Langkah 3 Jobsheet 6)

| Entitas | Atribut (**PK** dicetak tebal) | Catatan Batasan Integritas Data |
| :--- | :--- | :--- |
| **`pengguna`** | **`id`**, `username`, `password_hash`, `nama_lengkap`, `peran` | - `id`: Kunci utama otomatis (`AUTOINCREMENT`).<br>- `username`: Teks unik (`UNIQUE`), tidak boleh kosong (`NOT NULL`).<br>- `password_hash`: Hash kata sandi, tidak boleh kosong (`NOT NULL`).<br>- `nama_lengkap`: Teks nama kasir/pemilik (`NOT NULL`).<br>- `peran`: Teks dibatasi pilihan `CHECK (peran IN ('kasir', 'pemilik'))`, `NOT NULL`. |
| **`kategori`** | **`id`**, `nama` | - `id`: Kunci utama otomatis (`AUTOINCREMENT`).<br>- `nama`: Teks kategori unik (`UNIQUE`, misal: Makanan Utama, Sayur/Lauk, Minuman, Ekstra), `NOT NULL`. |
| **`menu`** | **`id`**, `kategori_id`, `nama`, `harga`, `status` | - `id`: Kunci utama otomatis (`AUTOINCREMENT`).<br>- `kategori_id`: Kunci asing (`REFERENCES kategori(id)`), `NOT NULL`.<br>- `nama`: Teks nama makanan/minuman unik (`UNIQUE`), `NOT NULL`.<br>- `harga`: Angka rupiah bulat `INTEGER >= 0`, batasan `CHECK (harga >= 0)`, `NOT NULL`.<br>- `status`: Teks pilihan `CHECK (status IN ('tersedia', 'habis'))`, nilai bawaan `'tersedia'`, `NOT NULL`. |
| **`transaksi`** | **`id`**, `nomor_transaksi`, `tanggal_waktu`, `tipe_pesanan`, `nomor_meja`, `metode_pembayaran`, `uang_diterima`, `pengguna_id` | - `id`: Kunci utama otomatis (`AUTOINCREMENT`).<br>- `nomor_transaksi`: Kode nota unik (`UNIQUE`, format `TRX-YYYYMMDD-XXX`), `NOT NULL`.<br>- `tanggal_waktu`: Teks format tanggal-waktu ISO (`YYYY-MM-DD HH:MM:SS`), `NOT NULL`.<br>- `tipe_pesanan`: Teks pilihan `CHECK (tipe_pesanan IN ('dine_in', 'take_away'))`, `NOT NULL`.<br>- `nomor_meja`: Teks/nomor meja (wajib diisi bila `dine_in`, boleh kosong bila `take_away`).<br>- `metode_pembayaran`: Teks pilihan `CHECK (metode_pembayaran IN ('tunai', 'qris'))`, `NOT NULL`.<br>- `uang_diterima`: Angka rupiah bulat `CHECK (uang_diterima >= 0)`.<br>- `pengguna_id`: Kunci asing (`REFERENCES pengguna(id)`), `NOT NULL`. |
| **`detail_transaksi`** | **`id`**, `transaksi_id`, `menu_id`, `jumlah`, `harga_satuan`, `catatan` | - `id`: Kunci utama otomatis (`AUTOINCREMENT`).<br>- `transaksi_id`: Kunci asing (`REFERENCES transaksi(id) ON DELETE CASCADE`), `NOT NULL`.<br>- `menu_id`: Kunci asing (`REFERENCES menu(id)`), `NOT NULL`.<br>- `jumlah`: Porsi pesanan `INTEGER > 0`, batasan `CHECK (jumlah > 0)`, `NOT NULL`.<br>- `harga_satuan`: Harga riil saat transaksi `INTEGER >= 0`, batasan `CHECK (harga_satuan >= 0)`, `NOT NULL`.<br>- `catatan`: Teks catatan pesanan (misal: "tidak pedas", "es batu dipisah"), boleh kosong (`NULL`). |

---

## 2. Penjelasan Kebijakan Atribut Non-Turunan (*Derived Attributes*)

Sesuai aturan baku Jobsheet 6 Bagian 2.1 & Langkah 3:
1. **Atribut Total Belanja Tidak Disimpan di Tabel `transaksi`:**
   - Total tagihan adalah nilai turunan yang dapat dihitung secara dinamis sewaktu-waktu menggunakan kueri agregasi:
     $$\text{Total Transaksi} = \sum (\text{detail\_transaksi.jumlah} \times \text{detail\_transaksi.harga\_satuan})$$
   - Mencegah anomali ketidaksinkronan data jika rincian item mengalami perubahan sebelum status transaksi final.
2. **Atribut Kembalian Tidak Disimpan:**
   - Kembalian dihitung langsung saat kasir menginput uang:
     $$\text{Kembalian} = \text{transaksi.uang\_diterima} - \text{Total Transaksi}$$
3. **Penyimpanan `harga_satuan` pada `detail_transaksi` Bukan Pelanggaran Normalisasi:**
   - Sebagaimana ditegaskan pada Jobsheet 6 Bagian 2.3: `harga_satuan` pada `detail_transaksi` mencatat **harga historis saat transaksi terjadi**. Jika di masa depan harga lauk pada tabel `menu` dinaikkan oleh pemilik warung, rekapitulasi nota dan omzet transaksi masa lalu tidak ikut berubah/rusak.
