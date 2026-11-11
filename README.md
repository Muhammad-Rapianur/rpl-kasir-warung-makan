# Sistem Kasir Warung Makan (KasirWarung)

Proyek tugas mata kuliah **Rekayasa Perangkat Lunak (RPL)** — Sistem informasi Point of Sales (POS) dan manajemen transaksi yang dirancang khusus untuk memenuhi kebutuhan operasional warung makan tradisional / UMKM kuliner.

---

## 📌 Ringkasan Dokumen Utama

1. **[Product Requirements Document (PRD)](PRD.md)**  
   Dokumen lengkap yang mendefinisikan latar belakang masalah, visi produk, target persona, ruang lingkup (In-Scope & Out-of-Scope), kebutuhan fungsional (FR), kebutuhan non-fungsional (NFR), arsitektur teknis, dan metrik keberhasilan (KPI).  
   *(Tersedia juga salinan di [docs/PRD.md](docs/PRD.md))*.

2. **[Aturan Proyek (Project Rules & Guidelines)](aturan-proyek.md)**  
   Pedoman tata kelola proyek yang mencakup standar branching Git, format pesan commit (*Conventional Commits*), konvensi kode Python/Flask/Jinja2, standar keamanan web (anti-XSS & anti-SQLi), aturan perumusan user story (INVEST & Given-When-Then), serta kriteria *Definition of Done* (DoD).  
   *(Tersedia juga salinan di [docs/aturan-proyek.md](docs/aturan-proyek.md))*.

3. **[Pemodelan Sistem dengan UML](docs/uml/README.md)**  
   Diagram Use Case, Skenario Use Case detail (UC-01 s.d. UC-07), dan 3 Activity Diagram proses utama dalam sintaks Mermaid (`flowchart LR` & `flowchart TD`).

4. **Dokumentasi Elisitasi Kebutuhan**
   - [Pedoman Wawancara](docs/elisitasi/pedoman-wawancara.md)
   - [Catatan Wawancara](docs/elisitasi/catatan-wawancara.md)
   - [User Story & Kriteria Penerimaan](docs/elisitasi/user-story.md)

---

## 🛠️ Rencana Teknologi (Tech Stack)
- **Backend:** Python 3.10+ & Flask
- **Frontend:** HTML5, CSS3 Modern, Jinja2 Templates (Desain responsif & touch-friendly)
- **Database:** SQLite3 (Penyimpanan lokal yang andal dan ringan)
- **Struk:** Browser Print Styling (`@media print`) kompatibel printer thermal 58mm/80mm

----

## 📂 Struktur Direktori Repositori
```text
rpl-kasir-warung-makan/
├── docs/
│   ├── elisitasi/            <-- Hasil riset: catatan wawancara, pedoman, & user story
│   │   ├── catatan-wawancara.md
│   │   ├── pedoman-wawancara.md
│   │   └── user-story.md
│   ├── uml/                  <-- Khusus berkas/gambar diagram UML (Use Case, Activity, dll.)
│   ├── PRD.md                <-- Dokumen Kebutuhan Produk (PRD)
│   └── aturan-proyek.md      <-- Pedoman tata kelola & standar proyek
├── .gitignore
├── aturan-proyek.md
├── PRD.md
└── README.md
```
