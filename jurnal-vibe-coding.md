# Jurnal Vibe Coding — Rekayasa Perangkat Lunak

- **Nama:** Muhammad Rapianur
- **NIM:** 24554010004
- **Topik / Jobsheet:** Jobsheet 9 — Kerangka Proyek dan Modul CRUD dengan Vibe Coding Terkendali

---

| No | Tujuan | Prompt (ringkas) | Hasil AI | Keputusan | Alasan |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | **[Siklus 1] Kerangka Proyek** | Konteks: `aturan-proyek.md` & `schema.sql`. Buat kerangka proyek Flask (`app.py`, `models.py` dengan `init_db()` & `PRAGMA foreign_keys = ON;`, `services.py`, `templates/base.html`). Batasan: pustaka standar + Flask, `SECRET_KEY` dari environment, redirect `/` ke `/menu`. | Dihasilkan 4 berkas kerangka lengkap. Basis data `kasir_warung.db` berhasil diinisialisasi otomatis dengan 5 tabel relasional. Pengujian rute `GET /` sukses redirect (302) ke `/menu` (200). | **Terima** | Arsitektur 3-tier rapi (pemisahan models, services, templates), kueri DDL terjaga utuh dari `schema.sql`, dan file `kasir_warung.db` aman diabaikan oleh `.gitignore`. |

---

> **Petunjuk Pengisian:**  
> - Setiap siklus enam langkah dicatat pada satu baris tabel di atas.
> - Kolom **Keputusan** diisi: `Terima`, `Ubah`, atau `Tolak`.
> - Kolom **Alasan** wajib memuat dasar teknis (kesesuaian kriteria penerimaan, arsitektur, keamanan, dsb.).
> - Minimal 8 siklus pada Jobsheet 9 (termasuk minimal 1 sesi berlabel `[Debug]`).
