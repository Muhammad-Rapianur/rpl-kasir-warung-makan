# Kesepakatan Tim (Team Working Agreement)
## Proyek: Sistem Kasir Warung Makan (KasirWarung)

Dokumen ini memuat kesepakatan internal, pembagian peran, aturan kerja sama, standar komunikasi, dan komitmen seluruh anggota tim pengembang dalam melaksanakan tugas mata kuliah **Rekayasa Perangkat Lunak (RPL)**.

---

### Informasi Tim Proyek
- **Mata Kuliah:** Rekayasa Perangkat Lunak
- **Nama Proyek:** Sistem Informasi Kasir & Manajemen Transaksi Warung Makan (*KasirWarung*)
- **Program Studi:** D3 Teknologi Informasi — Politeknik Sampit
- **Dosen Pengampu:** Achmad Afiffudin Nurzein, S.Kom
- **Koordinator RMK:** Oktama Pangestu, S.Kom
- **Tanggal Kesepakatan:** November 2026

---

## 1. Pembagian Peran & Tanggung Jawab (RACI Matrix)

Untuk memastikan akuntabilitas kerja, setiap peran memiliki tugas pokok dan matriks tanggung jawab yang jelas:

### 1.1 Struktur Peran Kelompok
1. **Product Owner / System Analyst:**
   - Bertanggung jawab memimpin wawancara elisitasi dengan pemilik warung makan, menyusun SRS dan PRD, serta memprioritaskan butir *Product Backlog*.
2. **Scrum Master / Git Coordinator:**
   - Bertanggung jawab mengatur jadwal sinkronisasi berkala, memantau *board* tugas di setiap Sprint, meninjau kepatuhan branching Git, serta mengelola proses integrasi Pull Request (PR).
3. **Lead Developer & Software Engineer:**
   - Bertanggung jawab merancang arsitektur backend Python Flask, struktur database SQLite, logika keranjang belanja, kalkulasi pembayaran, dan cetak struk thermal.
4. **Frontend & Usability Specialist:**
   - Bertanggung jawab mendesain antarmuka kasir yang responsif, *touch-friendly*, teks berkontras tinggi ($\ge 16\text{ px}$), serta dialog cetak peramban.
5. **Quality Assurance & Technical Writer:**
   - Bertanggung jawab menyiapkan skenario pengujian (*test cases*), memverifikasi hasil luaran AI, menyusun diagram UML, dan memperbarui catatan Jurnal *Vibe Coding*.

### 1.2 Matriks Tanggung Jawab (RACI)
- **R (Responsible):** Pelaksana tugas utama.
- **A (Accountable):** Penanggung jawab akhir hasil pekerjaan.
- **C (Consulted):** Rekan yang diajak berdiskusi/masukan sebelum tugas selesai.
- **I (Informed):** Anggota yang diberi tahu setelah tugas selesai.

| Komponen Pekerjaan | Analyst / PO | Scrum / Git | Lead Dev | Frontend | QA / Writer |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Elisitasi & Wawancara Klien | **A / R** | C | I | I | R |
| Dokumen SRS, PRD, & Aturan Proyek | **A / R** | C | C | C | R |
| Pemodelan UML (Use Case & Activity) | C | C | C | I | **A / R** |
| Product Backlog & Alokasi Sprint | **A / R** | R | C | C | I |
| Implementasi Backend (Flask & DB) | I | C | **A / R** | C | I |
| Implementasi Antarmuka Kasir (UI/UX) | I | I | C | **A / R** | C |
| Pengujian Skenario & Validasi Luaran AI | C | I | C | C | **A / R** |
| Code Review & Merge Pull Request | I | **A / R** | R | R | I |

---

## 2. Saluran & Ritme Komunikasi (Communication Cadence)

1. **Saluran Komunikasi Utama:**
   - **Grup Koordinasi Tim (WhatsApp / Telegram):** Saluran cepat untuk pengumuman harian, koordinasi mendesak, dan berbagi tautan PR.
   - **GitHub Repository (Pull Request & Issues):** Saluran resmi untuk tinjauan kode teknis, diskusi fitur, dan catatan revisi.
   - **Tatap Muka Praktikum & Lab:** Sinkronisasi mingguan di laboratorium komputer Politeknik Sampit untuk evaluasi tatap muka dan demonstrasi progres Sprint.
2. **Waktu Respons Komunikasi (Response Time SLA):**
   - Setiap anggota sepakat untuk merespons pesan penting terkait proyek di grup komunikasi maksimal dalam **4 jam kerja** (kecuali pada jam istirahat malam / perkuliahan lain).
3. **Sinkronisasi Berkala (*Standup Meeting*):**
   - Dilakukan 2 kali seminggu (durasi singkat 10–15 menit) untuk menjawab 3 pertanyaan dasar:
     1. Apa yang sudah diselesaikan kemarin?
     2. Apa yang akan dikerjakan hari ini?
     3. Kendala atau hambatan apa yang sedang dihadapi (*blocker*)?

---

## 3. Kesepakatan Alur Kerja Kolaborasi Git & Tinjauan Kode

1. **Larangan *Direct Push* ke Branch `main`:**
   - Branch `main` dilindungi (*protected*). Dilarang keras melakukan push kode langsung ke `main` tanpa melalui branch fitur dan peninjauan Pull Request.
2. **Aturan Penamaan Branch:**
   - Setiap pengerjaan tugas wajib membuat branch mandiri berformat: `docs-<nama-topik>` atau `feature/<nama-fitur>` (contoh: `docs-srs`, `docs-uml`, `docs-backlog`, `feature/pos-cart`).
3. **Ketentuan Pengajuan Pull Request (PR):**
   - Setiap PR wajib menggunakan templat [`.github/pull_request_template.md`](../../.github/pull_request_template.md) yang terisi lengkap (deskripsi, tag tipe perubahan, checklist kualitas, dan catatan peran AI).
4. **Waktu Tinjauan PR (*Review SLA*):**
   - Rekan satu tim wajib meninjau, menguji, dan memberikan tanggapan (*Approve* atau *Request Changes*) maksimal dalam **24 jam** setelah PR dibuka.
   - Suatu PR baru dapat di-merge setelah mendapat minimal **1 persetujuan (*approval*)** dari rekan satu tim yang tidak menulis kode tersebut.
5. **Standar Pesan Commit (*Conventional Commits*):**
   - Seluruh commit wajib menggunakan awalan baku: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, atau `chore:`.

---

## 4. Kesepakatan Pemanfaatan AI & Vibe Coding Terkendali

1. **Prinsip *Human-in-the-Loop*:**
   - Asisten AI digunakan untuk menyusun draf dokumen, mempercepat pembuatan templat, dan merapikan kode.
   - Setiap anggota tim bertanggung jawab penuh memahami 100% logika kode atau dokumen yang dihasilkan. Dilarang menyalin mentah-mentah (*copy-paste*) kode AI tanpa memahami alurnya.
2. **Transparansi Penggunaan AI:**
   - Setiap interaksi kunci, penolakan halusinasi AI, atau perbaikan manual wajib dicatat secara jujur pada deskripsi PR dan berkas **Jurnal Vibe Coding**.
3. **Kerahasiaan & Etika Data Klien:**
   - Dilarang menempelkan data pribadi nyata narasumber pemilik warung (nama pelanggan, kontak pribadi, data keuangan sensitif) ke kolom *prompt* AI publik. Seluruh data harus disamarkan atau dianonimkan terlebih dahulu.

---

## 5. Standar Kualitas Kerja (Definition of Done)

Sebuah butir tugas atau fitur resmi dianggap selesai (*Done*) apabila:
- [ ] Berjalan normal tanpa pesan kesalahan (*zero crash*) di lingkungan lokal Python Flask.
- [ ] Lolos pengujian skenario normal (*happy path*) dan kondisi batas (*edge cases*, misal: nominal bayar kurang, keranjang kosong).
- [ ] Tampilan antarmuka rapi, responsif, dan teks terbaca jelas (kontras tinggi, font $\ge 16\text{ px}$).
- [ ] Repositori tetap bersih dari berkas sampah (`.venv/`, `__pycache__/`, `.vscode/`) sesuai `.gitignore`.
- [ ] PR telah disetujui rekan peninjau dan berhasil digabungkan (*Merged*) ke branch `main`.

---

## 6. Manajemen Komitmen & Resolusi Hambatan (Conflict Resolution)

1. **Keterbukaan Hambatan Sejak Dini:**
   - Jika seorang anggota mengalami kesulitan teknis atau berhalangan hadir karena sakit/keperluan mendesak, anggota tersebut **wajib memberi kabar di grup minimal 1 hari sebelumnya** agar tugas dapat dialihkan atau dibantu bersama.
2. **Penyelesaian Perbedaan Pendapat:**
   - Perbedaan pendapat teknis (misal pemilihan struktur tampilan atau alur transaksi) diselesaikan dengan mengacu kembali pada **kebutuhan nyata klien di PRD/SRS** dan batasan waktu praktikum.
   - Jika musyawarah tim tidak mencapai kesepakatan, keputusan akhir diambil melalui fasilitasi bersama Dosen Pengampu atau Koordinator RMK RPL.

---

## 7. Pernyataan Komitmen Tim

Dengan disepakatinya dokumen ini, seluruh anggota tim berkomitmen untuk saling mendukung, bekerja sama secara profesional, menjaga integritas akademik, dan menyelesaikan seluruh target luaran praktikum **Sistem Kasir Warung Makan (*KasirWarung*)** tepat waktu hingga Ujian Akhir Semester.
