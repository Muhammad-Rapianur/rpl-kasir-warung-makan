# Catatan Perubahan

Format: [versi] - tanggal. Bagian: Ditambahkan, Diubah, Diperbaiki, Keamanan.

## [1.0.0] - 2026-11-20

### Ditambahkan
- Login dengan dua peran (**pemilik** dan **kasir**) beserta pembatasan hak akses per peran (RBAC decorator).
- Manajemen katalog menu makanan dan minuman (tambah, ubah, hapus, cari kata kunci, dan filter kategori/status ketersediaan).
- Manajemen kategori hidangan (makanan utama, sayur & lauk pauk, minuman, ekstra).
- Pencatatan transaksi penjualan kasir terhubung ke detail transaksi multi-item dengan kalkulasi total otomatis.
- Tampilan riwayat transaksi penjualan beserta rincian belanja per struk.
- Pencadangan basis data mandiri (`python cadangkan.py`) menggunakan SQLite Online Backup API ke folder `cadangan/`.
- Dukungan deployment server WSGI produksi via Waitress (`waitress-serve`).
- Nomor versi Semantic Versioning pada berkas `versi.py` dan ditampilkan di footer aplikasi web.

### Diperbaiki
- Hardening validasi angka: penolakan angka Unicode menggunakan `isascii() and isdigit()` (Cacat D-01).
- Penanganan Integer Overflow pada harga dan porsi dibatasi maksimal 1 Miliar / 10 digit (Cacat D-02).
- Pengetatan validasi format tanggal transaksi dengan pola baku ISO-8601 `YYYY-MM-DD` (Cacat D-03).
- Perlindungan penghapusan menu yang sudah memiliki relasi data pada transaksi penjualan.

### Keamanan
- Hashing kata sandi lambat menggunakan algoritma `scrypt` via Werkzeug dengan proteksi serangan pewaktuan (*anti-timing attack*).
- Perlindungan pemalsuan permintaan lintas situs (CSRF) pada setiap form transaksi POST.
- Pembatasan laju percobaan login (*sliding-window rate limiter*) dengan respons HTTP 429 Too Many Requests jika salah 5 kali berturut-turut.
- Penerapan header keamanan HTTP modern (`X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy`).
- Konfigurasi kunci rahasia sesi (`SECRET_KEY`) wajib berasal dari variabel lingkungan pada mode produksi.
