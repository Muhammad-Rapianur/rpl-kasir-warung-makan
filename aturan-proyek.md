# Aturan Proyek (Project Rules & Guidelines)
## Sistem Kasir Warung Makan (KasirWarung)

Dokumen ini memuat kesepakatan tata kelola, standar teknis, alur kerja Git, dan etika pengembangan yang wajib ditaati oleh pengembang dalam mengerjakan proyek tugas mata kuliah **Rekayasa Perangkat Lunak (RPL)**.

---

## 1. Prinsip Utama Pengembangan (Core Principles)

1. **Berpijak pada Masalah Nyata (*Reality-Grounded*):**
   - Setiap fitur yang dibangun harus berakar dari kebutuhan operasional riil warung makan (kecepatan pencatatan, kalkulasi kembalian akurat, cetak struk ringkas, dan rekap omzet harian).
   - Menghindari jebakan *over-engineering* atau penambahan fitur canggih yang tidak realistis bagi pelaku UMKM kuliner lokal (misalnya: tidak memaksakan integrasi e-commerce global, pemindai barcode, atau AI pembuat resep).

2. **Kritik & Kendali Penuh atas Kode AI (*Human-in-the-Loop*):**
   - Asisten AI digunakan sebagai akselerator koding dan penyusun draf logika, bukan penentu keputusan akhir.
   - Setiap kode, kueri SQL, atau template yang disarankan oleh AI wajib dipahami, diuji di lingkungan lokal, dan disesuaikan dengan batasan tugas sebelum digabungkan (*merged*) ke repositori.
   - Setiap iterasi prompt dan keputusan teknis dicatat secara berkala ke dalam jurnal proyek (*Jurnal Vibe Coding*).

3. **Integritas Akademik & Kerahasiaan Data:**
   - Dilarang mengunggah data pribadi sensitif milik narasumber/pemilik warung ke layanan publik (nama pelanggan, nomor telepon, data laba bersih riil wajib disamarkan atau dianonimkan).
   - Seluruh anggota memahami cara kerja sistem secara mendalam dan siap mempertanggungjawabkannya saat sesi evaluasi/presentasi proyek RPL.

---

## 2. Standar Git & Kolaborasi Repositori

### 2.1 Kebijakan Percabangan (*Branching Strategy*)
- **`main` (Protected/Production Branch):**
  - Hanya berisi kode yang sudah stabil, bebas error, dan siap didemokan kepada dosen/asisten pengampu.
  - Dilarang melakukan *direct push* secara sembrono ke branch `main` jika fitur baru belum teruji.
- **`feature/<nama-fitur>`:**
  - Setiap pengerjaan fungsionalitas baru wajib dibuat dalam branch terpisah.
  - Format penamaan:
    - `feature/pos-cart` (pengembangan keranjang pesanan kasir)
    - `feature/struk-cetak` (tampilan & cetak struk nota)
    - `feature/rekap-laporan` (modul ringkasan omzet harian)
    - `feature/manajemen-menu` (CRUD daftar lauk dan harga)
- **`fix/<nama-bug>`:**
  - Digunakan untuk perbaikan galat atau kesalahan kalkulasi (misal: `fix/kalkulasi-kembalian`).
- **`docs/<topik-dokumen>`:**
  - Digunakan untuk pembaruan berkas dokumentasi (misal: `docs/user-story`, `docs/prd`).

### 2.2 Format Pesan Commit (*Conventional Commits*)
Pesan commit harus ditulis secara jelas dan deskriptif menggunakan konvensi standar berikut:
```bash
<tipe>: <penjelasan singkat perubahan dalam bentuk kalimat aktif>
```
Daftar tipe commit yang diizinkan:
- `feat:` Penambahan fitur atau fungsionalitas baru (misal: `feat: tambah perhitungan kembalian otomatis di modul kasir`).
- `fix:` Perbaikan bug atau galat (misal: `fix: atasi kesalahan format tanggal pada nomor transaksi`).
- `docs:` Penambahan atau pembaruan dokumentasi (misal: `docs: selesaikan draf PRD dan user story`).
- `style:` Perapian gaya tampilan, spasi, atau formatting CSS tanpa mengubah logika sistem.
- `refactor:` Pengorganisasian ulang struktur kode tanpa menambah fitur baru atau mengubah output.
- `test:` Penambahan skenario pengujian atau uji manual.
- `chore:` Pembaruan dependensi, `.gitignore`, atau konfigurasi build.

### 2.3 Aturan Kebersihan Repositori (*Git Hygiene*)
- Berkas yang **dilarang keras** masuk ke commit Git:
  - Lingkungan virtual: `.venv/`, `env/`
  - Cache Python: `__pycache__/`, `*.pyc`
  - Berkas sesi editor lokal: `.vscode/`, `.idea/`
  - Berkas basis data sementara dengan data dummy acak: `*.db.tmp`
- Berkas `.gitignore` wajib dijaga dan dicek sebelum melakukan perintah `git add .`.

---

## 3. Konvensi Kode & Standar Kualitas

### 3.1 Backend (Python & Flask)
- Mengikuti pedoman penulisan kode **PEP 8**:
  - Penamaan fungsi dan variabel menggunakan `snake_case` (contoh: `hitung_kembalian()`, `total_tagihan`).
  - Penamaan kelas menggunakan `PascalCase` (contoh: `TransaksiManager`).
  - Penamaan konstanta menggunakan `UPPER_SNAKE_CASE` (contoh: `STATUS_TERSEDIA`).
- Menjaga fungsi tetap terfokus (*single responsibility*).
- Validasi input di sisi server: seluruh input angka (nominal pembayaran, harga makanan, kuantitas) harus diperiksa tipe datanya, nilai minimal `>= 0`, dan tidak membiarkan nilai `None` menyebabkan *crash* server.

### 3.2 Keamanan Web (*Web Security*)
- Mencegah celah **Cross-Site Scripting (XSS)**: Gunakan fasilitas *auto-escaping* bawaan Jinja2 (`{{ variable }}`). Hindari penggunaan filter `| safe` pada input yang berasal dari pengguna tanpa sanitasi ketat.
- Mencegah celah **SQL Injection**: Seluruh operasi database SQLite wajib memanfaatkan *parameterized queries* (menggunakan tanda `?` pada `sqlite3` atau melalui ORM) dan **dilarang menyambungkan string langsung** (*string concatenation*) ke dalam perintah SQL.

### 3.3 Frontend & Tampilan (HTML, CSS, JS)
- Desain antarmuka harus **responsif** dan **touch-friendly**: tombol menu memiliki ukuran area klik yang cukup besar untuk memudahkan operasional kasir via layar sentuh atau kursor laptop.
- Warna kontras tinggi untuk informasi krusial (total bayar, nominal kembalian, status pembayaran LUNAS).
- Styling khusus cetak (`@media print`) untuk menghasilkan struk yang rapi dan pas pada kertas struk mini thermal (lebar 58mm).

---

## 4. Aturan Elisitasi Kebutuhan & Dokumentasi

1. **Format User Story:**
   Seluruh *user story* yang ditulis pada `docs/elisitasi/user-story.md` harus memenuhi format baku:
   > "Sebagai **[peran/aktor]**, saya ingin **[tindakan/tujuan]**, agar **[manfaat/nilai bisnis]**."
2. **Kriteria INVEST:**
   Setiap user story harus diuji keterpenuhan kriteria **Independent, Negotiable, Valuable, Estimable, Small, Testable**.
3. **Kriteria Penerimaan Terukur (*Given–When–Then*):**
   Setiap user story wajib memiliki kriteria penerimaan yang jelas dan dapat diuji secara objektif, menyertakan angka/parameter konkret:
   - **Given** [kondisi awal]
   - **When** [aksi yang dilakukan pengguna]
   - **Then** [hasil atau respons yang diberikan sistem]
4. **Struktur Berkas Dokumentasi:**
   Dokumen analisis dan perancangan diletakkan di dalam folder `docs/`:
   - `docs/PRD.md` : Dokumen Kebutuhan Produk Utama.
   - `docs/aturan-proyek.md` : Aturan dan konvensi proyek.
   - `docs/elisitasi/` : Pedoman wawancara, catatan lapangan, dan daftar user story.
   - `docs/uml/` : Diagram alir, use case, dan class diagram.

---

## 5. Definisi Selesai (Definition of Done - DoD)

Suatu fitur atau modul dianggap **SELESAI (DONE)** hanya jika memenuhi seluruh daftar centang berikut:

- [ ] Kode fungsional berjalan tanpa galat pada lingkungan lokal Python Flask.
- [ ] Lolos pengujian skenario normal (*happy path*) sesuai kriteria *Given-When-Then*.
- [ ] Lolos pengujian skenario batas/ekstrem (*edge case*, misal: uang bayar kurang, keranjang kosong ditekan bayar).
- [ ] Tampilan halaman rapi, tidak terjadi elemen tumpang tindih (*layout break*) di browser laptop/tablet.
- [ ] Kode bersih dari komentar uji coba (*debug print*), rapi, dan mematuhi aturan penamaan.
- [ ] Kode berhasil di-commit ke Git dengan pesan commit yang terstandar (*Conventional Commits*).
- [ ] Dokumentasi terkait (status user story dan log keputusan vibe coding) telah diperbarui.
