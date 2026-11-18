# Jurnal Vibe Coding — Rekayasa Perangkat Lunak

- **Nama:** Muhammad Rapianur
- **NIM:** 24554010004
- **Topik / Jobsheet:** Jobsheet 9 — Kerangka Proyek dan Modul CRUD dengan Vibe Coding Terkendali

---

| No | Tujuan | Prompt (ringkas) | Hasil AI | Keputusan | Alasan |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **[Siklus 1] Kerangka Proyek** | Konteks: `aturan-proyek.md` & `schema.sql`. Buat kerangka proyek Flask (`app.py`, `models.py` dengan `init_db()` & `PRAGMA foreign_keys = ON;`, `services.py`, `templates/base.html`). Batasan: pustaka standar + Flask, `SECRET_KEY` dari environment, redirect `/` ke `/menu`. | Dihasilkan 4 berkas kerangka lengkap. Basis data `kasir_warung.db` berhasil diinisialisasi otomatis dengan 5 tabel relasional. Pengujian rute `GET /` sukses redirect (302) ke `/menu` (200). | **Terima** | Arsitektur 3-tier rapi (pemisahan models, services, templates), kueri DDL terjaga utuh dari `schema.sql`, dan file `kasir_warung.db` aman diabaikan oleh `.gitignore`. |
| **2** | **[Siklus 2] Daftar Data Menu** | Konteks: `models.py` & `schema.sql`. Buat fungsi `semua_menu()` dengan JOIN ke tabel `kategori` di `models.py`, rute `GET /menu` di `app.py`, dan `templates/menu_list.html` sesuai wireframe `wf-04`. Batasan: tidak ada kueri SQL di `app.py`, sediakan kondisi tabel kosong, format harga Rupiah. | Berhasil dibuat query JOIN kategori terurut nama menu, rute `GET /menu` tipis, dan tabel responsif dengan badge status Tersedia/Habis. Pengujian test client sukses 200 OK menampilkan data menu dan kategori. | **Terima** | Kode mematuhi pemisahan tanggung jawab (SQL hanya di models), kolom sesuai wireframe `wf-04`, dan aman terhadap XSS via Jinja2 auto-escaping. |

---

> **Petunjuk Pengisian:**  
> - Setiap siklus enam langkah dicatat pada satu baris tabel di atas.
> - Kolom **Keputusan** diisi: `Terima`, `Ubah`, atau `Tolak`.
> - Kolom **Alasan** wajib memuat dasar teknis (kesesuaian kriteria penerimaan, arsitektur, keamanan, dsb.).
> - Minimal 8 siklus pada Jobsheet 9 (termasuk minimal 1 sesi berlabel `[Debug]`).
