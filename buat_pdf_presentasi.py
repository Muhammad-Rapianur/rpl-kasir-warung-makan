"""Skrip pembuat dokumen PDF resmi Presentasi Praktikum RPL: KasirWarung v1.0.0.
Mahasiswa : Muhammad Rapianur (NIM: 24554010004)
Prodi     : D3 Teknologi Informasi, Politeknik Sampit
"""
import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Canvas kustom untuk menambahkan nomor halaman dan running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6c757d"))

        # Jangan gambar header di halaman 1 (Cover)
        if self._pageNumber > 1:
            self.drawString(40, 810, "Presentasi Praktikum RPL — KasirWarung v1.0.0 | Muhammad Rapianur (24554010004)")
            self.setStrokeColor(colors.HexColor("#ced4da"))
            self.setLineWidth(0.5)
            self.line(40, 804, 555, 804)

        # Footer di semua halaman
        teks_footer = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(555, 25, teks_footer)
        self.drawString(40, 25, "Politeknik Sampit — D3 Teknologi Informasi | Mata Kuliah RPL 2026")
        self.setStrokeColor(colors.HexColor("#ced4da"))
        self.setLineWidth(0.5)
        self.line(40, 35, 555, 35)
        self.restoreState()


def buat_pdf(output_path):
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Kustomisasi Styles
    primary_color = colors.HexColor("#0d47a1")
    secondary_color = colors.HexColor("#1b5e20")
    dark_neutral = colors.HexColor("#212529")

    style_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=8,
    )

    style_subtitle = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#495057"),
        alignment=1,
        spaceAfter=15,
    )

    style_meta = ParagraphStyle(
        "CoverMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=dark_neutral,
        alignment=1,
    )

    style_h1 = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
    )

    style_h2 = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
    )

    style_body = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=dark_neutral,
        spaceAfter=4,
    )

    style_body_bold = ParagraphStyle(
        "BodyDarkBold",
        parent=style_body,
        fontName="Helvetica-Bold",
    )

    style_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=dark_neutral,
    )

    style_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=style_cell,
        fontName="Helvetica-Bold",
    )

    style_cell_header = ParagraphStyle(
        "TableHeader",
        parent=style_cell,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )

    story = []

    # ==========================================
    # COVER / HEADER BANNER
    # ==========================================
    story.append(Paragraph("POLITEKNIK SAMPIT &mdash; PROGRAM STUDI D3 TEKNOLOGI INFORMASI", ParagraphStyle("HeaderKampus", alignment=1, fontName="Helvetica-Bold", fontSize=9, textColor=colors.HexColor("#6c757d"), spaceAfter=10)))
    story.append(Paragraph("PANDUAN &amp; MATERI PRESENTASI AKHIR RPL", style_title))
    story.append(Paragraph("Sistem Informasi Kasir Warung Makan (KasirWarung v1.0.0)", style_subtitle))
    story.append(Paragraph("<b>Mahasiswa:</b> Muhammad Rapianur (NIM: 24554010004) &nbsp;|&nbsp; <b>Dosen Pengampu:</b> Achmad Afiffudin Nurzein, S.Kom<br/><b>Mata Kuliah:</b> Rekayasa Perangkat Lunak (Semester 4 - 2026) &nbsp;|&nbsp; <b>Branch / Tag:</b> main (v1.0.0)", style_meta))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=12))

    # ==========================================
    # 1. TAHAPAN SDLC PADA PROYEK
    # ==========================================
    story.append(Paragraph("1&#xFE0F;&#x20E3; Tahapan SDLC pada Proyek KasirWarung", style_h1))
    story.append(Paragraph("Proyek dikerjakan secara berurutan dan disiplin melalui siklus hidup pengembangan perangkat lunak (SDLC) yang lengkap dengan bukti fisik artefak pada repositori:", style_body))

    sdlc_data = [
        [Paragraph("Tahapan SDLC", style_cell_header), Paragraph("Aktivitas yang Dikerjakan di Lapangan", style_cell_header), Paragraph("Bukti Konkret (Berkas Dokumen / Kode / Commit)", style_cell_header)],
        [
            Paragraph("<b>1. Elisitasi Kebutuhan</b>", style_cell),
            Paragraph("Wawancara dengan pemilik warung makan mitra, identifikasi alur transaksi meja kasir, dan penulisan user story.", style_cell),
            Paragraph("• docs/elisitasi/pedoman-wawancara.md<br/>• docs/elisitasi/catatan-wawancara.md<br/>• docs/elisitasi/user-story.md", style_cell)
        ],
        [
            Paragraph("<b>2. Analisis &amp; Spesifikasi</b>", style_cell),
            Paragraph("Mendefinisikan ruang lingkup (In/Out Scope), 13 Kebutuhan Fungsional (KF), 6 Kebutuhan Non-Fungsional (KNF), prioritas MoSCoW, dan matriks keterlacakan.", style_cell),
            Paragraph("• PRD.md (Product Requirements Document)<br/>• docs/srs/srs.md (Formal SRS)", style_cell)
        ],
        [
            Paragraph("<b>3. Perancangan Sistem</b>", style_cell),
            Paragraph("• UML: Use Case Diagram &amp; 3 Activity Diagram.<br/>• Data: ERD 5 entitas, Normalisasi 1NF-3NF, Kamus Data, DDL schema.sql.<br/>• Arsitektur 3-Tier &amp; Wireframe antarmuka (wf-01 s.d. wf-06).", style_cell),
            Paragraph("• docs/uml/use-case.mmd &amp; skenario-use-case.md<br/>• docs/desain/erd.mmd &amp; schema.sql<br/>• docs/desain/arsitektur.md<br/>• docs/desain/wireframe/", style_cell)
        ],
        [
            Paragraph("<b>4. Implementasi</b>", style_cell),
            Paragraph("Membangun backend Flask + SQLite terstruktur: presentation (app.py), business logic (services.py), data access (models.py), hashing scrypt, proteksi CSRF, dan RBAC.", style_cell),
            Paragraph("• app.py (455 baris), services.py, models.py<br/>• percobaan.py (Rate Limiter 429)<br/>• Commit: b43b81b, d054d0e, e02f1ed", style_cell)
        ],
        [
            Paragraph("<b>5. Pengujian (QA)</b>", style_cell),
            Paragraph("• 28 Test Case black-box (BVA &amp; EP).<br/>• 53 uji otomatis pytest terisolasi (tempfile in-memory DB) + 9 modul uji regresi cepat.<br/>• Perbaikan 3 cacat nyata (D-01 Unicode, D-02 Overflow, D-03 Tanggal).", style_cell),
            Paragraph("• docs/pengujian/test-case.md<br/>• tests/test_validasi.py, test_akses.py<br/>• docs/pengujian/laporan-cacat.md<br/>• Commit: ada34cd (47 pytest passed)", style_cell)
        ],
        [
            Paragraph("<b>6. Rilis dan UAT</b>", style_cell),
            Paragraph("Deployment server WSGI produksi Waitress, Semantic Versioning v1.0.0, dokumentasi README &amp; manual pengguna, UAT 6 skenario bersama klien (skor SUS 92.5).", style_cell),
            Paragraph("• versi.py, cadangkan.py, CHANGELOG.md<br/>• README.md &amp; docs/manual-pengguna.md<br/>• docs/uat/hasil-uat.md (Skor SUS 92.5)<br/>• Git Tag: v1.0.0 (Commit: 03d7e26)", style_cell)
        ],
    ]

    t_sdlc = Table(sdlc_data, colWidths=[105, 230, 180])
    t_sdlc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_sdlc)
    story.append(Spacer(1, 10))

    # ==========================================
    # 2. MODEL PROSES YANG DIPAKAI
    # ==========================================
    story.append(Paragraph("2&#xFE0F;&#x20E3; Model Proses yang Dipakai (Agile / Iteratif)", style_h1))
    story.append(Paragraph("<b>A. Perbedaan Waterfall vs Agile:</b><br/>"
                           "• <i>Waterfall:</i> Bersifat linear-sekuensial kaku (analisis selesai baru desain, desain selesai baru koding). Perubahan kebutuhan di tengah proyek sangat mahal dan produk baru bisa dilihat di akhir.<br/>"
                           "• <i>Agile (Iteratif-Inkremental):</i> Pengembangan dipecah ke dalam siklus-siklus pendek (Sprint). Setiap akhir siklus menghasilkan versi produk yang berfungsi (working increment), sehingga umpan balik klien langsung diintegrasikan.", style_body))
    story.append(Paragraph("<b>B. Mengapa Proyek KasirWarung Lebih Dekat ke Iteratif/Agile?</b><br/>"
                           "1. <b>Siklus Sprint Bertahap:</b> Sprint 1 (Fondasi DDL &amp; CRUD), Sprint 2 (Keamanan, RBAC, CSRF, Rate Limiting), Sprint 3 (QA Pytest, UAT, Rilis v1.0.0).<br/>"
                           "2. <b>Product Backlog Terkelola:</b> Fitur diprioritaskan via MoSCoW di <code>docs/backlog/product-backlog.md</code> dan disempurnakan tiap iterasi.<br/>"
                           "3. <b>Checkpoints Pengujian:</b> Setiap penambahan modul selalu diuji regresi via <code>tests/uji_cepat.py</code> sebelum melangkah ke tahap berikutnya.", style_body))
    story.append(Paragraph("<b>C. Penerapan Konsep Scrum pada Proyek Mandiri (Individu):</b><br/>"
                           "Meskipun dikerjakan perseorangan oleh Muhammad Rapianur, pilar utama Scrum tetap diterapkan: peran ganda (Product Owner &amp; Developer), pengelolaan Sprint Backlog, pelaksanaan Definition of Done (DoD) berbasis uji otomatis, dan evaluasi berkala via Jurnal Vibe Coding.", style_body))
    story.append(Spacer(1, 10))

    # ==========================================
    # 3. POSISI VIBE CODING DALAM SDLC
    # ==========================================
    story.append(Paragraph("3&#xFE0F;&#x20E3; Posisi Vibe Coding dalam SDLC", style_h1))
    story.append(Paragraph("<b>Peran AI dalam Rekayasa:</b> AI diposisikan sebagai <i>Pair Programmer</i> dan akselerator tugas repetitif (menulis draf kode awal, merancang variasi parameter uji pytest BVA/EP, dan merapikan CSS). AI <b>TIDAK</b> menggantikan pemikiran kritis insinyur perangkat lunak dalam menentukan arsitektur dan kontrol keamanan.", style_body))
    story.append(Paragraph("<b>Siklus Disiplin 6 Langkah:</b> Spesifikasi &rarr; Prompt Berkonteks Ketat &rarr; Generate &rarr; Jalankan &amp; Uji Cepat &rarr; Tinjau (Review Line-by-Line) &rarr; Commit &amp; Catat Jurnal.", style_body))

    vibe_summary = [
        [Paragraph("Metrik Jurnal Vibe Coding", style_cell_header), Paragraph("Nilai / Proporsi", style_cell_header), Paragraph("Keterangan Rekayasa", style_cell_header)],
        [Paragraph("Total Siklus Terekam", style_cell), Paragraph("<b>46 Siklus</b>", style_cell), Paragraph("Mencakup Jobsheet 9 s.d. 14 secara disiplin dan berkesinambungan", style_cell)],
        [Paragraph("Diterima (Terima)", style_cell), Paragraph("<b>43 Siklus (93,5%)</b>", style_cell), Paragraph("Output AI mematuhi kaidah arsitektur 3-tier, OWASP, dan lulus uji otomatis", style_cell)],
        [Paragraph("Diubah Mandiri (Ubah)", style_cell), Paragraph("<b>3 Siklus (6,5%)</b>", style_cell), Paragraph("Penyesuaian format Rupiah, perbaikan docstring, dan koreksi encoding UTF-16 BOM", style_cell)],
        [Paragraph("Ditolak (Tolak)", style_cell), Paragraph("<b>0 Siklus (0%)</b>", style_cell), Paragraph("Prompt modular dengan batasan domain warung makan mencegah halusinasi kode", style_cell)],
    ]
    t_vibe = Table(vibe_summary, colWidths=[130, 110, 275])
    t_vibe.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_vibe)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Contoh Nyata dari Jurnal:</b><br/>"
                           "• <b>Keputusan 'Ubah' (Siklus 43):</b> AI menghasilkan berkas <code>requirements.txt</code> dengan encoding UTF-16 LE BOM Windows sehingga pytest gagal <code>UnicodeDecodeError</code>. Pengembang mendeteksi galat ini lewat otomasi uji dan menulis ulang file ke format UTF-8 standar.<br/>"
                           "• <b>Keputusan 'Terima' (Siklus 34):</b> AI menyarankan filter <code>teks.isascii() and teks.isdigit()</code> untuk menutup celah Cacat D-01 (karakter Unicode '²'). Solusi langsung meluluskan uji unit tanpa efek samping.", style_body))

    story.append(Paragraph("<b>Risiko Vibe Coding &amp; Strategi Pengendaliannya:</b><br/>"
                           "1. <i>Kode Tidak Dipahami:</i> Dikendalikan dengan membaca diff kode baris per baris sebelum commit dan mencatat alasan teknis di jurnal.<br/>"
                           "2. <i>Kerentanan Keamanan:</i> Dikendalikan dengan audit keamanan OWASP 2025 (seluruh query SQL parameterized '?', CSRF token aktif, scrypt hash).<br/>"
                           "3. <i>Uji Palsu (False Green):</i> Dikendalikan dengan <b>Uji Mutasi Manual</b> (sengaja merusak batas kode validasi untuk memastikan uji gagal).", style_body))
    story.append(Spacer(1, 10))

    # ==========================================
    # 4. SKENARIO & PANDUAN DEMO APLIKASI
    # ==========================================
    story.append(Paragraph("4&#xFE0F;&#x20E3; Skenario &amp; Panduan Demo Aplikasi", style_h1))
    story.append(Paragraph("Aplikasi dapat dijalankan melalui server produksi Waitress (<code>waitress-serve --listen=127.0.0.1:8000 app:app</code>) atau mode pengembangan (<code>python app.py</code>) dengan data dummy menu warung makan yang realistis.", style_body))

    demo_steps = [
        [Paragraph("Peran / Skenario", style_cell_header), Paragraph("Langkah Uji Coba Demonstrasi", style_cell_header), Paragraph("Hasil yang Diharapkan (Expected Outcome)", style_cell_header)],
        [
            Paragraph("<b>Alur Kasir</b><br/>(siti_kasir / siti12345)", style_cell),
            Paragraph("1. Login sebagai kasir.<br/>2. Periksa bahwa tombol <i>+ Tambah Menu</i> &amp; menu <i>Kategori</i> TIDAK MUNCUL.<br/>3. Catat pesanan: Ayam Bakar (2) + Es Teh (2).<br/>4. Klik Simpan Transaksi.<br/>5. Coba ketik manual URL: <code>/menu/tambah</code>.", style_cell),
            Paragraph("• Total belanja Rp 46.000 terhitung otomatis.<br/>• Transaksi tersimpan di riwayat kasir.<br/>• Akses ke /menu/tambah <b>DITOLAK DENGAN HALAMAN 403 FORBIDDEN</b>.", style_cell)
        ],
        [
            Paragraph("<b>Alur Pemilik</b><br/>(pak_joko / joko12345)", style_cell),
            Paragraph("1. Login sebagai pemilik.<br/>2. Periksa tombol <i>+ Tambah Menu</i> &amp; menu <i>Kategori</i> MUNCUL.<br/>3. Buka Riwayat Transaksi.<br/>4. Tambah menu baru: Bebek Bakar Madu (Rp 28.000).", style_cell),
            Paragraph("• Hak akses manajerial terbuka penuh.<br/>• Seluruh transaksi kasir terlihat transparan.<br/>• Menu baru langsung muncul di katalog kasir.", style_cell)
        ],
        [
            Paragraph("<b>Uji Keamanan</b><br/>(Rate Limiter 429)", style_cell),
            Paragraph("Di form login, masukkan kata sandi salah sebanyak 6 kali berturut-turut.", style_cell),
            Paragraph("Pada percobaan ke-6, sistem memblokir request dengan respons <b>HTTP 429 Too Many Requests</b> (anti brute-force).", style_cell)
        ],
    ]
    t_demo = Table(demo_steps, colWidths=[105, 235, 175])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_demo)
    story.append(Spacer(1, 10))

    # ==========================================
    # 5. MATRIKS KESIAPAN PENILAIAN DOSEN
    # ==========================================
    story.append(Paragraph("5&#xFE0F;&#x20E3; Matriks Kesiapan Penilaian Dosen", style_h1))
    eval_rubric = [
        [Paragraph("Kriteria Penilaian", style_cell_header), Paragraph("Kondisi Nyata pada Proyek KasirWarung", style_cell_header), Paragraph("Status", style_cell_header)],
        [
            Paragraph("Ketepatan Tahapan SDLC", style_cell),
            Paragraph("Terpenuhi dari wawancara elisitasi, PRD/SRS, UML/ERD, 3-Tier, Pytest QA, hingga rilis v1.0.0.", style_cell),
            Paragraph("<b>LENGKAP 100%</b>", style_cell)
        ],
        [
            Paragraph("Keterkaitan Teori &amp; Proyek", style_cell),
            Paragraph("Penerapan Agile Scrum, arsitektur 3-tier, OWASP 2025, dan BVA/EP terhubung nyata ke domain warung makan.", style_cell),
            Paragraph("<b>SESUAI TEORI</b>", style_cell)
        ],
        [
            Paragraph("Bukti Fisik Konkret", style_cell),
            Paragraph("53 uji pytest passed, 9 uji regresi lolos, 46 entri jurnal, git tag v1.0.0, dan dokumen UAT SUS 92.5.", style_cell),
            Paragraph("<b>TERVERIFIKASI</b>", style_cell)
        ],
        [
            Paragraph("Pemahaman Vibe Coding", style_cell),
            Paragraph("Memahami 6 siklus rekayasa, membuktikan koreksi mandiri atas cacat/encoding AI, dan mitigasi risiko.", style_cell),
            Paragraph("<b>SANGAT BAIK</b>", style_cell)
        ],
        [
            Paragraph("Kesesuaian Aplikasi dgn PRD", style_cell),
            Paragraph("Seluruh kebutuhan fungsional (KF-01 s.d. KF-13) dan non-fungsional berjalan lancar tanpa cacat blokir.", style_cell),
            Paragraph("<b>SIAP DEMO</b>", style_cell)
        ],
    ]
    t_eval = Table(eval_rubric, colWidths=[140, 305, 70])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#ced4da")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_eval)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUKSES] Dokumen PDF presentasi berhasil dibuat di: {output_path}")


if __name__ == "__main__":
    target = Path(r"d:\RPL\rpl-kasir-warung-makan\docs\presentasi-kasirwarung.pdf")
    target.parent.mkdir(parents=True, exist_ok=True)
    buat_pdf(target)
