# Jurnal Vibe Coding — Rekayasa Perangkat Lunak

- **Nama:** Muhammad Rapianur
- **NIM:** 24554010004
- **Topik / Jobsheet:** Jobsheet 9 — Kerangka Proyek dan Modul CRUD dengan Vibe Coding Terkendali

---

| No | Tujuan | Prompt (ringkas) | Hasil AI | Keputusan | Alasan |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **[Siklus 1] Kerangka Proyek** | Konteks: `aturan-proyek.md` & `schema.sql`. Buat kerangka proyek Flask (`app.py`, `models.py` dengan `init_db()` & `PRAGMA foreign_keys = ON;`, `services.py`, `templates/base.html`). Batasan: pustaka standar + Flask, `SECRET_KEY` dari environment, redirect `/` ke `/menu`. | Dihasilkan 4 berkas kerangka lengkap. Basis data `kasir_warung.db` berhasil diinisialisasi otomatis dengan 5 tabel relasional. Pengujian rute `GET /` sukses redirect (302) ke `/menu` (200). | **Terima** | Arsitektur 3-tier rapi (pemisahan models, services, templates), kueri DDL terjaga utuh dari `schema.sql`, dan file `kasir_warung.db` aman diabaikan oleh `.gitignore`. |
| **2** | **[Siklus 2] Daftar Data Menu** | Konteks: `models.py` & `schema.sql`. Buat fungsi `semua_menu()` dengan JOIN ke tabel `kategori` di `models.py`, rute `GET /menu` di `app.py`, dan `templates/menu_list.html` sesuai wireframe `wf-04`. Batasan: tidak ada kueri SQL di `app.py`, sediakan kondisi tabel kosong, format harga Rupiah. | Berhasil dibuat query JOIN kategori terurut nama menu, rute `GET /menu` tipis, dan tabel responsif dengan badge status Tersedia/Habis. Pengujian test client sukses 200 OK menampilkan data menu dan kategori. | **Terima** | Kode mematuhi pemisahan tanggung jawab (SQL hanya di models), kolom sesuai wireframe `wf-04`, dan aman terhadap XSS via Jinja2 auto-escaping. |
| **3** | **[Siklus 3] Tambah Data Menu** | Konteks: `app.py`, `models.py`, `services.py`. Buat form tambah menu (`GET` & `POST /menu/tambah`), fungsi validasi server di `services.py` (nama wajib $\ge 2$ karakter, harga $> 0$), fungsi `tambah_menu()` berparameter di `models.py`, dan `templates/menu_form.html`. Batasan: pola Post-Redirect-Get, *flash message*, tangani nama duplikat (`IntegrityError`). | Dihasilkan fungsi validasi server, kueri `INSERT` berparameter `?`, serta rute form lengkap. Diuji pada 5 skenario (valid, nama kosong, harga $-5$, harga non-angka `'abc'`, dan nama duplikat `Ayam Goreng`); seluruh 5 uji **LULUS (100%)**. | **Terima** | Memenuhi kriteria F3 & KF-02; validasi sisi server mencegah anomali data; isian form tidak hilang saat terjadi galat; bebas injeksi SQL. |
| **4** | **[Siklus 4] Ubah Data Menu** | Konteks: `app.py`, `models.py`, `templates/menu_form.html`. Buat fitur ubah menu di rute `GET` dan `POST /menu/<id>/ubah`, fungsi `ambil_menu()` dan `ubah_menu()` di `models.py`. Batasan: form terisi data lama via `dict(menu)`, status ketersediaan dapat diubah (*tersedia/habis*), ID tidak ada $\rightarrow$ 404, tangani nama duplikat. | Ditambahkan rute update dan kueri SQL `UPDATE` berparameter. Diuji: data lama terisi di form, pembaruan sukses tampil di tabel, nama duplikat ditolak, dan ID fiktif `/menu/999/ubah` mengembalikan status 404 Not Found. Semua uji lulus. | **Terima** | Memenuhi kriteria F4 & KF-02; penanganan 404 sesuai standar REST; konversi `dict(menu)` mencegah crash; arsitektur berlapis tetap konsisten. |
| **5** | **[Siklus 5] Hapus Data Menu** | Konteks: `app.py`, `models.py`, `schema.sql`. Buat fitur hapus menu di rute `POST /menu/<id>/hapus` dan fungsi `hapus_menu()` di `models.py`. Batasan: hanya izinkan metode `POST` (tolak `GET`), tangani `sqlite3.IntegrityError` jika menu sudah dirujuk `detail_transaksi`, ID fiktif $\rightarrow$ 404. | Dihasilkan rute hapus dengan penanganan `IntegrityError`. Diuji 4 kasus: `GET /menu/1/hapus` ditolak (405 Method Not Allowed), menu bebas berhasil dihapus, menu terikat transaksi gagal aman dengan notifikasi ramah, dan ID 999 menghasilkan 404. | **Terima** | Memenuhi kriteria F5 & KF-02; kunci asing `ON DELETE RESTRICT` aktif dan aman; pencegahan penghapusan via `GET` melindungi data dari *crawling* peramban. |

---

> **Petunjuk Pengisian:**  
> - Setiap siklus enam langkah dicatat pada satu baris tabel di atas.
> - Kolom **Keputusan** diisi: `Terima`, `Ubah`, atau `Tolak`.
> - Kolom **Alasan** wajib memuat dasar teknis (kesesuaian kriteria penerimaan, arsitektur, keamanan, dsb.).
> - Minimal 8 siklus pada Jobsheet 9 (termasuk minimal 1 sesi berlabel `[Debug]`).
