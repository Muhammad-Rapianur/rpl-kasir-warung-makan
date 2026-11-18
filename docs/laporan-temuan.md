# Laporan Temuan Code Review & Keamanan Dasar
**Mata Kuliah:** Rekayasa Perangkat Lunak (Jobsheet 12)  
**Kelompok Proyek:** KasirWarung (D3 TI Politeknik Sampit)  
**Penyusun:** Muhammad Rapianur (NIM: 24554010004)  

---

## 1. Analisis Kasus Latihan (kasus_rentan.py — Lampiran B.1)

| No | Lokasi Kode | Masalah Keamanan | Kategori OWASP Top 10:2025 | Dampak Eksploitasi | Tingkat Risiko |
| :---: | :--- | :--- | :---: | :--- | :---: |
| **(1)** | `import flask_auth_helperz` | Mengimpor paket fiktif/halusinasi AI yang tidak resmi di PyPI. | **A03: Software Supply Chain Failures** | Penyerang dapat mendaftarkan nama paket tersebut di PyPI dan menyisipkan kode berbahaya (*supply chain attack*). | **Tinggi** |
| **(2)** | `app.secret_key = "rahasia123"` | Kunci rahasia sesi ditulis langsung (*hardcoded*) di kode program. | **A02: Security Misconfiguration** | Sesi cookie dapat dipalsukan oleh siapa saja yang membaca kode di repositori publik. | **Tinggi** |
| **(3)** | `hashlib.md5(p.encode()).hexdigest()` | Menggunakan algoritma hash MD5 yang cepat dan tanpa garam (*salt*). | **A04: Cryptographic Failures** | Kata sandi mudah dibongkar dalam hitungan detik menggunakan *Rainbow Table* atau GPU cracking. | **Tinggi** |
| **(4)** | `f"... WHERE username='{u}' ..."` | Query SQL dirakit menggunakan f-string langsung dari masukan form. | **A05: Injection (SQL Injection)** | Penyerang dapat bypass login tanpa kata sandi atau menghapus seluruh tabel database. | **Kritis / Tinggi** |
| **(5)** | `"Kata sandi salah untuk pengguna " + u` | Pesan kesalahan login membocorkan status validitas nama pengguna. | **A07: Authentication Failures** | Membantu penyerang memetakan daftar akun terdaftar (*username enumeration*). | **Sedang** |
| **(6)** | `redirect(request.args["next"])` | Parameter `next` langsung dialihkan tanpa validasi domain internal. | **A01: Broken Access Control (Open Redirect)** | Pengguna dapat dijebak dialihkan ke situs *phishing* berbahaya setelah login berhasil. | **Sedang** |
| **(7)** | `@app.route("/barang/<int:id>/hapus")` | Hapus data dapat diakses via metode `GET` tanpa login dan tanpa CSRF token. | **A01: Broken Access Control** | Siapa pun (bahkan web crawler peramban) dapat menghapus barang hanya dengan membuka link. | **Tinggi** |
| **(8)** | `@app.route("/catatan/<int:id>")` | Mengambil data catatan berdasarkan ID tanpa memeriksa kepemilikan pengguna. | **A01: Broken Access Control (IDOR)** | Pengguna biasa dapat membaca catatan rahasia milik pengguna lain hanya dengan mengganti angka ID di URL. | **Tinggi** |
| **(9)** | `except Exception as e: return f"Galat: {e!r}"` | Menampilkan repr galat mentah dan traceback internal ke layar pengguna. | **A10: Mishandling of Exceptional Conditions** | Membocorkan struktur tabel, nama kolom, dan versi sistem basis data ke penyerang. | **Rendah-Sedang** |
| **(10)** | `app.run(host="0.0.0.0", debug=True)` | Mode debug interaktif aktif dan mengikat ke seluruh antarmuka jaringan IP publik. | **A02: Security Misconfiguration** | Konsol debug interaktif Werkzeug dapat dieksekusi penyerang untuk menjalankan perintah remote shell (*RCE*). | **Kritis / Tinggi** |

---

## 2. Bukti Tiga Kerentanan Kasus Latihan (Langkah 4)

### Bukti 1: SQL Injection Bypass Login (Nomor 4)
* **Masukan Uji:**  
  * Username: `' OR '1'='1' --`
  * Password: `sembarang`
* **Hasil Nyata:**  
  Kueri SQL menjadi: `SELECT id, peran FROM pengguna WHERE username='' OR '1'='1' --' AND password_hash='...'`.  
  Kondisi `'1'='1'` bernilai benar dan tanda komentar `--` membuang pengecekan password. Penyerang berhasil login langsung sebagai akun pertama di database tanpa mengetahui password asli.

### Bukti 2: Hapus Data via Metode GET Tanpa Autentikasi (Nomor 7)
* **Langkah Reproduksi:**  
  Buka peramban atau jalankan curl: `curl http://localhost:5000/barang/1/hapus`.
* **Hasil Nyata:**  
  Data barang dengan `id=1` langsung terhapus permanen dari basis data SQLite tanpa ada permintaan login atau token CSRF sama sekali.

### Bukti 3: Open Redirect Phishing (Nomor 6)
* **Langkah Reproduksi:**  
  Akses URL: `http://localhost:5000/login?next=https://situs-pencuri.example`.
* **Hasil Nyata:**  
  Setelah pengguna memasukkan username dan password yang benar, aplikasi langsung mengeluarkan header `Location: https://situs-pencuri.example`, mengalihkan pengguna keluar situs ke domain penipuan.

---

## 3. Laporan Temuan Keamanan pada Proyek Sendiri (KasirWarung — Langkah 7)

Berikut adalah 5 temuan keamanan pada proyek KasirWarung yang ditriase untuk diperbaiki pada Jobsheet 12 Sesi 2:

### T-01: Ketiadaan Proteksi Cross-Site Request Forgery (CSRF) pada Form POST
- **Lokasi:** `app.py` pada seluruh rute `methods=["POST"]` dan template formulir.
- **Kategori:** A01: Broken Access Control.
- **Deskripsi:** Form transaksi, tambah menu, ubah menu, dan hapus menu belum menyertakan token acak sinkronisasi CSRF. Penyerang dapat membuat halaman web jahat yang mengirimkan request POST otomatis saat kasir membuka web tersebut.
- **Bukti:** Pengiriman request POST via cURL tanpa token diterima dengan status 200/302.
- **Dampak:** Aksi manipulasi menu atau pencatatan transaksi fiktif dapat dipicu tanpa disadari oleh pengguna yang sedang login.
- **Tingkat Risiko:** **Tinggi**.
- **Usulan Perbaikan:** Terapkan mekanisme token CSRF berbasis sesi acak `secrets.token_hex(16)` dan verifikasi pada `before_request`.
- **Status:** **Diperbaiki hari ini (Langkah 11)**.

### T-02: Belum Ada Pembatasan Percobaan Login Gagal (Brute-Force Attack)
- **Lokasi:** `app.py:login()`.
- **Kategori:** A07: Authentication Failures.
- **Deskripsi:** Penyerang dapat mencoba ratusan kombinasi kata sandi tanpa ada jeda atau pemblokiran akun.
- **Bukti:** Pengujian mengirimkan 50 request POST login gagal secara beruntun tetap diproses server tanpa penolakan.
- **Dampak:** Kata sandi akun kasir atau pemilik berpotensi ditebak via serangan kamus (*dictionary attack*).
- **Tingkat Risiko:** **Sedang**.
- **Usulan Perbaikan:** Tambahkan modul `percobaan.py` untuk membatasi maksimal 5 kegagalan per 5 menit per kombinasi IP + username (HTTP 429).
- **Status:** **Diperbaiki hari ini (Langkah 12)**.

### T-03: Ketiadaan Audit Logging untuk Kejadian Keamanan Kritis
- **Lokasi:** `app.py`.
- **Kategori:** A09: Security Logging & Alerting Failures.
- **Deskripsi:** Percobaan login gagal dan insiden akses terlarang (403 Forbidden) tidak dicatat ke log sistem.
- **Bukti:** Terminal hanya mencetak log standar HTTP dari Werkzeug tanpa identitas username atau keterangan insiden.
- **Dampak:** Jika terjadi pembobolan akun, administrator warung tidak memiliki bukti jejak audit forensik.
- **Tingkat Risiko:** **Sedang**.
- **Usulan Perbaikan:** Integrasikan modul `logging` untuk mencatat login gagal, login terkunci, dan akses 403 dengan format aman `%r`.
- **Status:** **Diperbaiki hari ini (Langkah 12)**.

### T-04: Ketiadaan Header Respons Keamanan Standar
- **Lokasi:** `app.py:after_request`.
- **Kategori:** A02: Security Misconfiguration.
- **Deskripsi:** Server belum mengirimkan header perlindungan peramban standar seperti anti-clickjacking dan MIME sniffing.
- **Bukti:** Header respons HTTP tidak memuat `X-Frame-Options` maupun `X-Content-Type-Options`.
- **Dampak:** Aplikasi dapat dimuat di dalam `<iframe>` situs penipu (*clickjacking*).
- **Tingkat Risiko:** **Rendah-Sedang**.
- **Usulan Perbaikan:** Tambahkan middleware `after_request` yang menyuntikkan `X-Frame-Options: DENY` dan `X-Content-Type-Options: nosniff`.
- **Status:** **Diperbaiki hari ini (Langkah 13)**.

### T-05: Konfigurasi Mode Produksi dan Fail-Secure SECRET_KEY
- **Lokasi:** `app.py:app.secret_key`.
- **Kategori:** A02: Security Misconfiguration.
- **Deskripsi:** Nilai `SECRET_KEY` memiliki fallback default `"dev-only-..."` yang berisiko jika dijalankan di server produksi tanpa sengaja.
- **Bukti:** Aplikasi tetap berjalan meskipun variabel `SECRET_KEY` tidak diatur di lingkungan sistem operasi.
- **Dampak:** Cookie sesi dapat didekripsi jika kunci default dipakai di lingkungan publik.
- **Tingkat Risiko:** **Tinggi (pada produksi)**.
- **Usulan Perbaikan:** Hentikan aplikasi dengan `RuntimeError` jika `APP_ENV=production` dan `SECRET_KEY` tidak diisi.
- **Status:** **Diperbaiki hari ini (Langkah 13)**.
