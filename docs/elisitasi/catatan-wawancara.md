# Catatan Hasil Wawancara Elisitasi Kebutuhan Sistem KasirWarung

> **Tanggal Pelaksanaan:** 4 November 2026 (Pukul 15.30 &ndash; 16.45 WIB)  
> **Lokasi:** Warung Makan Selera Nusantara, Jl. Tjilik Riwut KM 3, Baamang, Sampit  
> **Pewawancara:** Muhammad Rapianur (NIM: 24554010004)  
> **Narasumber:**  
> 1. **Pak Joko** &mdash; Pemilik Warung Makan (*Owner*)  
> 2. **Mbak Siti** &mdash; Petugas Kasir / Pelayan Utama

---

## 1. Profil Usaha Mitra
* **Nama Usaha:** Warung Makan Selera Nusantara (Sampit)
* **Jenis Usaha:** Warung makan prasmanan dan pesanan masakan khas Nusantara (Nasi Goreng, Ayam Bakar, Ikan Goreng, Aneka Sayur, dan Es Minuman).
* **Volume Transaksi:** 100 &ndash; 160 transaksi per hari (puncak keramaian pada pukul 11.30 &ndash; 13.30 saat jam makan siang pekerja kantoran dan mahasiswa).
* **Perangkat Saat Ini:** 1 unit laptop Windows di meja kasir, 1 kalkulator fisik, dan buku nota rangkap karbon.

---

## 2. Transkrip &amp; Catatan Poin Wawancara

### Sesi Bersama Mbak Siti (Petugas Kasir)

* **Pewawancara:** *"Mbak Siti, bagaimana alur saat jam makan siang ramai, dan bagaimana cara menghitung total belanja pembeli?"*  
  * **Mbak Siti:** *"Kalau jam makan siang itu antrean meja kasir bisa sampai 5-8 orang berdiri nunggu bayar. Pelanggan biasanya nyebutin apa saja yang dimakan: nasi putih, ayam bakar, tempe goreng, sama es teh manis. Saya ngitung pakai kalkulator tangan. Kadang kalau terburu-buru, ada harga lauk yang lupa atau salah ketik angka di kalkulator. Waktu ngitung kembalian juga sering bikin tegang kalau uangnya pecahan Rp 100.000."*

* **Pewawancara:** *"Berapa lama rata-rata waktu yang dibutuhkan untuk melayani satu orang pembeli di kasir?"*  
  * **Mbak Siti:** *"Kalau pesanan banyak lauknya, bisa sampai 1 sampai 1,5 menit per orang cuma buat ngitung total dan ngasih kembalian. Pelanggan di belakang kadang sudah kelihatan tidak sabar."*

* **Pewawancara:** *"Bagaimana dengan nota kertas bon yang ditulis?"*  
  * **Mbak Siti:** *"Sering basah mas, kan meja kasir dekat meja minum es atau kuah sayur. Kertas bon sobek atau tintanya luntur. Kadang sobekan bon terselip di laci uang, pas malam mau dihitung pemilik suka kurang kertasnya."*

* **Pewawancara:** *"Kalau ada sistem kasir di laptop, tampilan seperti apa yang Mbak Siti harapkan?"*  
  * **Mbak Siti:** *"Tolong jangan yang rumit mas. Saya bukan anak IT. Pengennya tinggal pilih nama makanan dari daftar atau ketik sedikit langsung muncul, porsinya bisa diisi angka, total rupiahnya keluar sendiri otomatis. Tombolnya harus besar dan jelas."*

---

### Sesi Bersama Pak Joko (Pemilik Warung)

* **Pewawancara:** *"Pak Joko, apa kendala paling berat yang dihadapi dari sisi pengelolaan keuangan dan menu?"*  
  * **Pak Joko:** *"Masalah paling utama itu pas tutup warung malam hari jam 9 malam. Saya harus duduk ngumpulin sobekan bon kertas, ngitung pakai kalkulator satu-satu untuk tahu omzet hari ini. Itu makan waktu 45 menit sampai 1 jam sendiri padahal badan sudah capek. Sering juga uang di laci fisik selisih puluhan ribu dibanding catatan bon."*

* **Pewawancara:** *"Bagaimana kebijakan perubahan harga menu di warung ini?"*  
  * **Pak Joko:** *"Harga cabai atau daging ayam sering naik-turun. Kalau harga ayam bakar saya naikkan dari Rp 16.000 ke Rp 18.000, kadang kasir lupa dan masih narik harga lama ke pelanggan. Saya rugi. Jadi saya ingin kalau harga saya ganti di komputer, kasir langsung otomatis pakai harga baru."*

* **Pewawancara:** *"Terkait hak akses sistem, apakah kasir boleh mengedit harga makanan?"*  
  * **Pak Joko:** *"Jangan! Kasir cuma boleh input pesanan pembeli dan lihat menu saja. Jangan sampai kasir bisa ganti-ganti harga makanan atau hapus kategori seenaknya. Yang boleh ganti harga atau hapus hidangan cuma saya sebagai pemilik."*

* **Pewawancara:** *"Bagaimana dengan kondisi jaringan internet di warung?"*  
  * **Pak Joko:** *"Internet di sini kadang sinyalnya drop atau mati lampu. Saya tidak mau aplikasi kasir yang bergantung internet penuh. Kalau internet mati kasir harus tetap jalan melayani pelanggan, cukup jalan di laptop kasir atau jaringan lokal toko saja."*

---

## 3. Matriks Analisis Masalah &amp; Kebutuhan Solusi (*Problem-to-Need Mapping*)

| No | Temuan Masalah Lapangan (*Pain Points*) | Kebutuhan Solusi Sistem (*System Requirements*) |
|:--:|---|---|
| 1 | Antrean kasir lambat (&gt;60 detik) akibat hitung kalkulator manual. | Fitur formulir transaksi kasir otomatis: subtotal dan total langsung dikalkulasi sistem dalam hitungan detik. |
| 2 | Kasir salah menghitung uang kembalian pada jam sibuk. | Fitur kalkulator bayar dan kembalian otomatis saat kasir memasukkan nominal uang terima. |
| 3 | Kertas nota fisik mudah rusak, basah, tercecer, dan hilang. | Pencatatan transaksi digital berbasis basis data lokal SQLite dengan nomor struk unik (`TRX-YYYYMMDD-XXX`). |
| 4 | Rekapitulasi omzet harian memakan waktu 45-60 menit setiap malam. | Halaman riwayat transaksi dan ringkasan omzet otomatis yang dapat dilihat pemilik dalam 1 klik. |
| 5 | Ketidaksesuaian penetapan harga antara pemilik dan kasir. | Katalog menu terpusat: harga yang tampil di kasir dikendalikan secara mutlak dari master data pemilik. |
| 6 | Risiko kasir mengubah harga sepihak atau mengakses fitur sensitif. | Kontrol akses berbasis peran (RBAC) dengan 2 peran: **Pemilik** (akses penuh) dan **Kasir** (akses transaksi saja). |
| 7 | Koneksi internet tidak stabil di lokasi warung. | Arsitektur lokal (*offline-first / local server*), menggunakan Python Flask + SQLite tanpa ketergantungan API awan eksternal. |
| 8 | Risiko manipulasi data kasir dari luar atau serangan brute force. | Autentikasi aman password hash scrypt, proteksi CSRF, dan pembatasan salah login 5 kali (Rate Limiting HTTP 429). |

---

## 4. Kesimpulan Hasil Elisitasi
Berdasarkan hasil wawancara mendalam di atas, disepakati bahwa sistem **KasirWarung** harus mengutamakan:
1. **Kecepatan dan Kesederhanaan Antarmuka (*Speed &amp; Simplicity*):** Kasir dapat menyelesaikan transaksi dalam waktu &le; 15 detik.
2. **Pemisahan Peran yang Tegas (*Strict RBAC*):** Membatasi akses menu master dan kategori hanya untuk Pemilik, sedangkan Kasir fokus pada operasional penjualan.
3. **Keandalan Lokal (*High Availability*):** Sistem beroperasi secara offline/lokal tanpa biaya hosting bulanan, aman, dan data tersimpan otomatis.
