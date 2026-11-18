# Catatan Temuan Keamanan Autentikasi & Otorisasi — KasirWarung
*Mata Kuliah: Rekayasa Perangkat Lunak (Jobsheet 11 - Langkah 7)*

Daftar temuan keamanan berikut ditinjau berdasarkan daftar periksa Lampiran C.2 dan rujukan OWASP Top 10:2025:

| No | Kategori Temuan | Tingkat Risiko | Deskripsi Temuan & Dampak | Tindakan yang Diterapkan / Direncanakan |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Pembatasan Percobaan Login (*Rate Limiting*)** | Sedang | Rute `POST /login` belum membatasi jumlah percobaan login gagal. Penyerang dapat mencoba serangan *brute-force* secara berulang. | **Ditunda untuk Pertemuan 12:** Implementasi Flask-Limiter atau counter percobaan gagal per IP/username. |
| **2** | **Proteksi Pemalsuan Permintaan Lintas Situs (*CSRF Token*)** | Sedang | Form `POST` (seperti hapus menu dan catat transaksi) belum memuat token acak CSRF tersembunyi. | **Ditunda untuk Pertemuan 12:** Penerapan modul `Flask-WTF` CSRFProtect atau token sinkron di cookie sesi. |
| **3** | **Atribut Cookie Produksi (*Secure Flag*)** | Rendah (saat dev lokal) | Pengaturan `SESSION_COOKIE_SECURE` belum diaktifkan karena lingkungan laboratorium berjalan di HTTP lokal (`http://localhost:5000`). | **Direncanakan:** Diaktifkan otomatis via environment flag saat deployment HTTPS di Pertemuan 14. |
| **4** | **Pencegahan Timing Attack** | Tinggi | Username yang tidak terdaftar berpotensi terdeteksi via waktu respons verifikasi hash yang berbeda. | **SELESAI DITERAPKAN:** Digunakan `_HASH_PALSU` pada `services.autentikasi()` sehingga waktu komputasi identik. |
| **5** | **Pencegahan Open Redirect** | Tinggi | Parameter URL `?next=...` dapat dieksploitasi untuk memancing kasir ke situs phising luar. | **SELESAI DITERAPKAN:** Fungsi `_tujuan_aman()` memvalidasi bahwa URL harus diawali satu garis miring `/` (internal situs). |
