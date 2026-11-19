# KasirWarung — Sistem Informasi Kasir Warung Makan

Aplikasi web kasir dan manajemen penjualan sederhana yang dirancang khusus untuk memenuhi kebutuhan operasional warung makan tradisional dan UMKM kuliner.

Dibuat sebagai proyek mata kuliah **Rekayasa Perangkat Lunak (RPL)**, Program Studi D3 Teknologi Informasi, **Politeknik Sampit**.  
Pengembang: **Muhammad Rapianur** (NIM: **24554010004**)  
Versi saat ini: **1.0.0** (lihat [CHANGELOG.md](CHANGELOG.md)).

---

## 🚀 Fitur Utama

- **Autentikasi & Kontrol Akses Dua Peran (RBAC):**
  - **👑 Pemilik Warung:** Akses penuh mencakup katalog menu hidangan, manajemen kategori, pencatatan transaksi, dan riwayat laporan penjualan.
  - **🧾 Kasir:** Akses operasional untuk transaksi penjualan dan melihat katalog ketersediaan menu makanan/minuman (dibatasi dari aksi perubahan data master).
- **Katalog Menu & Kategori:**
  - Pengelompokan hidangan (Makanan Utama, Sayur & Lauk Pauk, Minuman, Ekstra & Camilan).
  - Pencarian aman kata kunci hidangan (anti-SQL Injection) dan penyaringan status ketersediaan (*tersedia* / *habis*).
- **Pencatatan Transaksi Kasir Multi-Item:**
  - Kalkulasi subtotal dan total belanja otomatis dalam satu transaksi atomik.
- **Pencadangan Mandiri (Online Backup):**
  - Skrip pencadangan SQLite aman tanpa perlu menghentikan aplikasi (`python cadangkan.py`).
- **Keamanan Web Berlapis:**
  - Password hashing lambat `scrypt` via Werkzeug dengan pertahanan *anti-timing attack*.
  - Proteksi CSRF berbasis token unik per sesi.
  - *Sliding-window rate limiter* login (HTTP 429 Too Many Requests jika salah 5 kali berturut-turut).
  - Header keamanan peramban (`nosniff`, `SAMEORIGIN`, CSP).

---

## 📋 Kebutuhan Sistem

- **Python:** Versi 3.10 atau lebih baru (direkomendasikan Python 3.12+)
- **Sistem Operasi:** Windows 10/11 atau Linux
- **Git:** Untuk kloning dan manajemen versi repositori

---

## ⚙️ Instalasi

1. **Kloning Repositori:**
   ```powershell
   git clone https://github.com/Muhammad-Rapianur/rpl-kasir-warung-makan.git
   cd rpl-kasir-warung-makan
   ```

2. **Buat & Aktifkan Virtual Environment:**
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * **Linux/macOS:**
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```

3. **Pasang Dependensi Terkunci:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

---

## 🔐 Konfigurasi (Variabel Lingkungan)

Konfigurasi aplikasi diatur murni melalui variabel lingkungan (tanpa rahasia tertulis di kode program):

| Variabel | Fungsi | Nilai Bawaan | Keterangan |
|---|---|---|---|
| `APP_ENV` | Mode operasional aplikasi | (kosong = development) | Atur `production` untuk mode rilis resmi |
| `SECRET_KEY` | Kunci enkripsi sesi pengguna | `dev-only-kasir-warung-2026` | **Wajib diisi acak pada mode produksi** |
| `KASIR_DB` / `TOKO_DB` | Lokasi berkas basis data SQLite | `kasir_warung.db` di root proyek | Jalur absolut/relatif file database |
| `COOKIE_SECURE` | Pengiriman cookie sesi | `1` pada produksi, `0` dev | Atur `0` jika diakses via HTTP jaringan lokal |

> 💡 **Cara Membuat Kunci Acak Kuat:**
> ```powershell
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

## 👤 Membuat Akun Pengguna Pertama

Jalankan skrip pembuat akun interaktif:
```powershell
python buat_pengguna.py
```
Masukkan nama pengguna, peran (`pemilik` atau `kasir`), nama lengkap, dan kata sandi (minimal 8 karakter). Kata sandi dibaca tersembunyi tanpa ditampilkan di layar dan langsung di-hash menggunakan `scrypt`.

---

## ▶️ Menjalankan Aplikasi

### 1. Mode Pengembangan (Development)
```powershell
python app.py
```
Aplikasi berjalan di: 👉 **`http://127.0.0.1:5000`**

### 2. Mode Produksi (WSGI Waitress)
```powershell
# Atur variabel lingkungan di Windows PowerShell:
$env:APP_ENV="production"
$env:SECRET_KEY="<masukkan_kunci_acak_32_byte>"
$env:COOKIE_SECURE="0"  # bila memakai HTTP di jaringan lokal toko

# Jalankan server Waitress:
waitress-serve --listen=127.0.0.1:8000 app:app
```
Aplikasi produksi berjalan di: 👉 **`http://127.0.0.1:8000`**

*Untuk akses dari komputer/perangkat lain di jaringan lokal tertutup, ganti `--listen=0.0.0.0:8000` dan izinkan port 8000 pada Windows Firewall.*

---

## 🧪 Pengujian Otomatis

Pasang dependensi pengujian (`pytest==9.1.1`):
```powershell
python -m pip install -r requirements-dev.txt
```

Jalankan seluruh suite uji otomatis:
```powershell
# Uji unit, validasi, otorisasi peran, integrasi alur, dan kebersihan rilis (53 uji):
python -m pytest -v tests/test_pertama.py tests/test_validasi.py tests/test_akses.py tests/test_alur_transaksi.py tests/test_rilis.py

# Uji regresi keamanan cepat (CSRF, Rate Limit 429, Security Header, RBAC):
python tests/uji_cepat.py
```

---

## 💾 Pencadangan dan Pemulihan (Backup & Restore)

- **Mencadangkan Basis Data:**
  ```powershell
  python cadangkan.py
  ```
  Berkas cadangan akan disimpan di folder `cadangan/` dengan format nama `kasir-YYYYMMDD-HHMMSS.db`. Skrip ini aman dijalankan secara berkala saat kasir sedang aktif melayani pesanan.

- **Memulihkan Basis Data (Restore):**
  1. Hentikan proses aplikasi (`CTRL+C`).
  2. Salin berkas cadangan ke nama database aktif:
     ```powershell
     Copy-Item cadangan/kasir-<stempel-waktu>.db kasir_warung.db -Force
     ```
  3. Jalankan kembali aplikasi kasir.

---

## 📁 Struktur Direktori

```text
rpl-kasir-warung-makan/
├── app.py                  # Presentation Layer: Route Flask, Session, RBAC, Header
├── services.py             # Business Logic Layer: Validasi input, kalkulasi, hashing
├── models.py               # Data Access Layer: Parameterized SQL Queries
├── percobaan.py            # Rate Limiter Sliding Window (HTTP 429)
├── versi.py                # Definisi konstanta Semantic Versioning
├── cadangkan.py            # Modul pencadangan database mandiri (SQLite Backup API)
├── buat_pengguna.py        # Skrip CLI pembuat akun pengguna ber-hash scrypt
├── requirements.txt        # Kunci versi dependensi produksi (termasuk waitress)
├── requirements-dev.txt    # Dependensi khusus pengujian pengembang (pytest)
├── CHANGELOG.md            # Catatan perubahan rilis versi
├── static/                 # Berkas statis CSS antarmuka
├── templates/              # Berkas template Jinja2 (HTML)
├── tests/                  # Suite pengujian otomatis (53 uji pytest + uji cepat)
└── docs/                   # Dokumentasi PRD, SRS, UML, Desain, Pengujian, & Manual
    ├── manual-pengguna.md  # Buku panduan pengguna bergambar untuk kasir & pemilik
    ├── rilis/              # Lembar audit kesiapan rilis (Lampiran B)
    └── uat/                # Bukti pelaksanaan UAT, perhitungan SUS, & triase
```

---

## 🧪 Catatan Hasil "Uji Orang Asing" (Stranger Test)

Dokumentasi `README.md` ini telah diuji coba pada lingkungan bersih (*clean machine/new venv*) oleh rekan sejawat independen:
- **Penguji:** Rekan Mahasiswa D3 TI Politeknik Sampit
- **Hasil:** Berhasil mengkloning, membuat venv, memasang `requirements.txt`, mengonfigurasi variabel lingkungan, menjalankan aplikasi lewat `waitress-serve`, hingga login dan mencatat transaksi penjualan tanpa asistensi manual.
- **Catatan Perbaikan:** Ditambahkan penjelasan perintah PowerShell spesifik Windows (`$env:APP_ENV=...`) agar pengguna Windows tidak bingung dengan format perintah `export` bawaan Linux.

---

## 👥 Pengembang & Hak Cipta

- **Pengembang:** Muhammad Rapianur (NIM: 24554010004)
- **Program Studi:** D3 Teknologi Informasi, Politeknik Sampit
- **Mata Kuliah:** Rekayasa Perangkat Lunak (Semester 4 - 2026)
- **Dosen Pengampu:** Achmad Afiffudin Nurzein, S.Kom
