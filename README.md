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

3. **[Software Requirements Specification (SRS)](docs/srs/srs.md)**  
   Dokumen spesifikasi kebutuhan perangkat lunak formal (13 Kebutuhan Fungsional berawalan *"Sistem harus..."*, 6 Kebutuhan Non-Fungsional terukur, MoSCoW, batasan, asumsi, dan matriks keterlacakan).  
   *(Tersedia di folder [docs/srs/](docs/srs/) dan salinan di [docs/srs.md](docs/srs.md))*.

4. **[Pemodelan Sistem dengan UML](docs/uml/README.md)**  
   Diagram Use Case, Skenario Use Case detail (UC-01 s.d. UC-07), dan 3 Activity Diagram proses utama dalam sintaks Mermaid (`flowchart LR` & `flowchart TD`).

5. **[Product Backlog & Rencana Sprint](docs/backlog/product-backlog.md)**  
   Daftar tugas terkelola (*Product Backlog*), pemetaan prioritas MoSCoW ke Sprint 1–4, rincian tugas harian Sprint 1 (T-1.1 s.d. T-1.8), dan kriteria *Definition of Done*.  
   *(Tersedia di folder [docs/backlog/](docs/backlog/) dan salinan di [docs/product-backlog.md](docs/product-backlog.md))*.

6. **Dokumentasi Elisitasi Kebutuhan**
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
├── .github/
│   └── pull_request_template.md  <-- Templat PR standar mata kuliah RPL
├── docs/
│   ├── backlog/              <-- 📂 Manajemen Product Backlog & Rencana Sprint
│   │   ├── README.md
│   │   └── product-backlog.md
│   ├── elisitasi/            <-- Hasil riset: catatan wawancara, pedoman, & user story
│   │   ├── catatan-wawancara.md
│   │   ├── pedoman-wawancara.md
│   │   └── user-story.md
│   ├── srs/                  <-- Dokumen Spesifikasi Kebutuhan Perangkat Lunak (SRS)
│   │   ├── README.md
│   │   └── srs.md
│   ├── uml/                  <-- Khusus berkas diagram UML (Use Case, Activity, dll.)
│   │   ├── activity-01-transaksi-penjualan.mmd
│   │   ├── activity-02-kelola-menu.mmd
│   │   ├── activity-03-rekap-omzet.mmd
│   │   ├── README.md
│   │   ├── skenario-use-case.md
│   │   └── use-case.mmd
│   ├── product-backlog.md    <-- Salinan langsung Product Backlog di docs/
│   ├── srs.md                <-- Salinan langsung SRS di folder docs/
│   ├── PRD.md                <-- Dokumen Kebutuhan Produk (PRD)
│   └── aturan-proyek.md      <-- Pedoman tata kelola & standar proyek
├── .gitignore
├── aturan-proyek.md
├── PRD.md
└── README.md
```
