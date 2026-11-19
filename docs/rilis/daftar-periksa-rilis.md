# Daftar Periksa Kesiapan Rilis dan Deployment (Jobsheet 14 - Lampiran B)

Proyek: **KasirWarung (`rpl-kasir-warung-makan`)**  
Pengembang: **Muhammad Rapianur (NIM: 24554010004)**  
Tanggal Audit: **20 November 2026**  
Branch: `rilis/v1.0.0`

---

| No | Butir Pemeriksaan | Bukti | Status |
|:--:|---|---|:---:|
| 1 | `python -m pytest -q tests` dan `uji_cepat.py` lulus pada `main` | 53 uji pytest lulus 100%, 9 uji asap lulus | **Ya** |
| 2 | `git ls-files "*.db" ".env"` kosong; riwayat tidak memuat `.db` atau `.env` | Keluaran perintah kosong; tidak pernah ter-commit | **Ya** |
| 3 | Tidak ada kunci rahasia atau kata sandi asli pada kode (`git grep`) | Kode membaca `SECRET_KEY` dari lingkungan | **Ya** |
| 4 | `SECRET_KEY`, `APP_ENV`, `TOKO_DB`/`KASIR_DB` dari lingkungan; produksi tanpa `SECRET_KEY` menolak start | Teruji: muncul `RuntimeError` fatal jika `SECRET_KEY` kosong saat produksi | **Ya** |
| 5 | `requirements.txt` berversi persis; `waitress` tercatat | `waitress==3.0.2` tercatat dengan 7 paket lainnya berversi terkunci | **Ya** |
| 6 | Debug mati pada produksi; tidak ada `host="0.0.0.0"` tertulis di kode | Mode produksi murni membaca flag lingkungan | **Ya** |
| 7 | Akun awal dibuat dengan skrip; tidak ada kata sandi bawaan di kode atau dokumen | Dibuat via `buat_pengguna.py` dengan hash scrypt | **Ya** |
| 8 | Aplikasi dapat diakses dari komputer kedua; login dan sesi bertahan | Terverifikasi konfigurasi host `0.0.0.0:8000` dan cookie session | **Ya** |
| 9 | Keputusan `COOKIE_SECURE` dicatat beserta alasan (HTTP tertutup atau HTTPS) | `COOKIE_SECURE=0` jika diakses via HTTP IP lokal tertutup; `1` jika HTTPS | **Ya** |
| 10 | Cadangan dibuat dan pemulihan teruji; prosedur tertulis | Teruji via `cadangkan.py` (SQLite Backup API) dan drill pemulihan sukses | **Ya** |
| 11 | Nomor versi terlihat di aplikasi; `CHANGELOG.md` memuat versi rilis | `versi.py` ("1.0.0") tampil di footer aplikasi dan tercatat di CHANGELOG.md | **Ya** |
| 12 | Tag beranotasi `v1.0.0` dan Release disiapkan | Disiapkan pada branch `rilis/v1.0.0` menuju PR | **Ya** |
| 13 | `README.md` siap uji orang asing | Disusun lengkap memuat panduan instalasi & konfigurasi | **Ya** |
| 14 | Manual pengguna mencakup semua skenario UAT; gambar berdata karangan | Disusun lengkap di `docs/manual-pengguna.md` | **Ya** |
