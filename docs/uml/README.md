# Pemodelan Sistem dengan UML (KasirWarung)

Folder ini berisi artefak pemodelan sistem perangkat lunak untuk **Sistem Kasir Warung Makan (*KasirWarung*)**, disusun berdasarkan acuan **Jobsheet 5 Praktikum Rekayasa Perangkat Lunak**.

---

## 📋 Daftar Isi Berkas
1. [`use-case.mmd`](use-case.mmd) : Kode sumber Mermaid Use Case Diagram sistem kasir warung makan.
2. [`skenario-use-case.md`](skenario-use-case.md) : Dokumen skenario detail 6 *use case* (alur utama, alternatif, dan pengecualian).
3. [`activity-01-transaksi-penjualan.mmd`](activity-01-transaksi-penjualan.mmd) : Activity Diagram proses pencatatan penjualan kasir & pembayaran.
4. [`activity-02-kelola-menu.mmd`](activity-02-kelola-menu.mmd) : Activity Diagram proses tambah & pembaruan menu makanan/minuman.
5. [`activity-03-rekap-omzet.mmd`](activity-03-rekap-omzet.mmd) : Activity Diagram proses penutupan kas & rekapitulasi omzet harian.

---

## 1. Identifikasi Aktor (Langkah 2 Jobsheet 5)

| No | Aktor | Deskripsi Peran | Sumber (PRD/SRS) |
| :-: | :--- | :--- | :--- |
| 1 | **Kasir** | Petugas operasional yang melayani pesanan pembeli di meja kasir, memilih menu pesanan, menerima pembayaran (Tunai/QRIS), menghitung uang kembalian, dan mencetak struk nota. | PRD Bagian 3, FR-03 s.d. FR-08 |
| 2 | **Pemilik** | Pengelola usaha yang mengatur daftar menu beserta harga, mengontrol ketersediaan menu lauk harian, serta memantau laporan omzet dan rekap kas harian. | PRD Bagian 3, FR-01, FR-02, FR-10, FR-11 |

---

## 2. Tabel Pemetaan Use Case (Langkah 3 Jobsheet 5)

| ID | Nama Use Case | Aktor | Kebutuhan Terkait (KF) | Prioritas |
| :-: | :--- | :--- | :--- | :-: |
| **UC-01** | Login Sistem | Kasir, Pemilik | FR-01, NFR-Security | Must |
| **UC-02** | Mencatat Transaksi Penjualan | Kasir | FR-03, FR-04, FR-05, FR-06, FR-07, FR-12 | Must |
| **UC-03** | Cek Ketersediaan Menu | Kasir | FR-01, FR-02 (via include UC-02) | Must |
| **UC-04** | Mencetak Struk Pembayaran | Kasir | FR-08 (via extend UC-02) | Must |
| **UC-05** | Mengelola Data Menu | Pemilik | FR-01, FR-02 | Must |
| **UC-06** | Melihat Riwayat Transaksi | Kasir, Pemilik | FR-09 | Should |
| **UC-07** | Melihat Rekapitulasi Omzet | Pemilik | FR-10, FR-11 | Must |

---

## 3. Visualisasi Diagram

### A. Use Case Diagram
```mermaid
flowchart LR
    Kasir[["Aktor: Kasir"]]
    Pemilik[["Aktor: Pemilik"]]

    subgraph S["Sistem Kasir Warung Makan (KasirWarung)"]
        UC1(["UC-01: Login Sistem"])
        UC2(["UC-02: Mencatat Transaksi Penjualan"])
        UC3(["UC-03: Cek Ketersediaan Menu"])
        UC4(["UC-04: Mencetak Struk Pembayaran"])
        UC5(["UC-05: Mengelola Data Menu"])
        UC6(["UC-06: Melihat Riwayat Transaksi"])
        UC7(["UC-07: Melihat Rekapitulasi Omzet"])
    end

    Kasir --- UC1
    Kasir --- UC2
    Kasir --- UC6

    Pemilik --- UC1
    Pemilik --- UC5
    Pemilik --- UC6
    Pemilik --- UC7

    UC2 -.->|include| UC3
    UC4 -.->|extend| UC2
```

---

### B. Activity Diagram 1: Pencatatan Transaksi Penjualan
```mermaid
flowchart TD
    A((Mulai)) --> B[Kasir membuka halaman POS]
    B --> C[Kasir memilih jenis pesanan: Dine-in / Bungkus]
    C --> D[Kasir memilih menu makanan/minuman]
    D --> E{Menu tersedia?}
    
    E -- Tidak --> F[Sistem menampilkan pesan menu habis]
    F --> D
    
    E -- Ya --> G[Sistem menambahkan item ke keranjang dan hitung subtotal]
    G --> H{Ada menu lain yang ingin dipesan?}
    H -- Ya --> D
    H -- Tidak --> I[Kasir menekan tombol proses pembayaran]
    
    I --> J{Metode pembayaran?}
    
    J -- Tunai --> K[Kasir memasukkan jumlah uang yang diterima]
    K --> L{Uang diterima mencukupi?}
    L -- Tidak --> M[Sistem menampilkan peringatan uang kurang]
    M --> K
    L -- Ya --> N[Sistem menghitung nominal uang kembalian]
    N --> P[Sistem menyimpan transaksi ke database]
    
    J -- QRIS --> Q[Sistem menampilkan kode QR statis warung]
    Q --> R[Pelanggan memindai QRIS dan kasir verifikasi status bayar]
    R --> P
    
    P --> S[Sistem membuat nomor transaksi unik dan struk digital]
    S --> T{Pelanggan meminta struk cetak?}
    T -- Ya --> U[Sistem mengirim perintah cetak ke printer thermal]
    U --> V((Selesai))
    T -- Tidak --> V
```

---

### C. Activity Diagram 2: Pengelolaan Data Menu
```mermaid
flowchart TD
    A((Mulai)) --> B[Pemilik membuka halaman manajemen menu]
    B --> C[Sistem menampilkan daftar menu eksisting]
    C --> D{Pilih aksi kelola menu?}
    
    D -- Tambah Baru --> E[Pemilik mengisi form nama menu, kategori, harga, dan status]
    E --> F[Pemilik menekan tombol simpan menu]
    F --> G{Harga berupa angka positif?}
    G -- Tidak --> H[Sistem menampilkan pesan validasi harga tidak valid]
    H --> E
    G -- Ya --> I{Nama menu sudah terdaftar?}
    I -- Ya --> J[Sistem menampilkan peringatan nama menu duplikat]
    J --> E
    I -- Tidak --> K[Sistem menyimpan menu baru ke database]
    
    D -- Ubah / Edit --> L[Pemilik memilih menu dan mengubah harga atau status]
    L --> M[Pemilik menekan tombol perbarui menu]
    M --> N{Format perubahan valid?}
    N -- Tidak --> O[Sistem menampilkan pesan galat validasi]
    O --> L
    N -- Ya --> P[Sistem memperbarui data menu di database]
    
    K --> Q[Sistem menampilkan notifikasi sukses dan memperbarui tabel menu]
    P --> Q
    Q --> R((Selesai))
```

---

### D. Activity Diagram 3: Rekapitulasi Omzet Harian
```mermaid
flowchart TD
    A((Mulai)) --> B[Pemilik membuka halaman laporan penjualan]
    B --> C{Pilih filter periode?}
    
    C -- Hari Ini --> D[Sistem mengambil seluruh transaksi tanggal hari ini]
    C -- Rentang Tanggal --> E[Pemilik memilih tanggal awal dan tanggal akhir]
    E --> F[Sistem mengambil transaksi sesuai rentang tanggal]
    
    D --> G{Terdapat transaksi tercatat?}
    F --> G
    
    G -- Tidak --> H[Sistem menampilkan informasi: Belum ada transaksi / Omzet Rp0]
    H --> I((Selesai))
    
    G -- Ya --> J[Sistem menghitung total akumulasi omzet kotor]
    J --> K[Sistem memisahkan rincian penerimaan: Kas Tunai vs Saldo QRIS]
    K --> L[Sistem menyusun daftar 5 menu terlaris beserta jumlah porsi]
    L --> M[Sistem merender kartu ringkasan omzet dan grafik/tabel penjualan]
    M --> N[Pemilik melakukan pencocokan fisik uang laci dengan rekap kas]
    N --> I
```

---

## 4. Daftar Periksa Verifikasi (Lampiran C Jobsheet 5)

| No | Pertanyaan Periksa | Hasil Evaluasi |
| :-: | :--- | :--- |
| 1 | Semua aktor di diagram ada di PRD? Adakah aktor tambahan? | **Lolos.** Aktor hanya `Kasir` dan `Pemilik`, tanpa aktor fiktif. |
| 2 | Setiap use case tertelusur ke minimal satu KF? | **Lolos.** Seluruh UC terhubung ke FR-01 s.d. FR-12 di PRD. |
| 3 | Adakah use case tambahan yang tidak ada di PRD? | **Lolos.** Tidak ada fitur liar/halusinasi seperti pemindai barcode atau e-commerce kurir. |
| 4 | Notasi benar: aktor di luar batas sistem, include/extend tepat? | **Lolos.** Aktor di luar kotak subgraph. Relasi `include` untuk validasi menu, `extend` untuk cetak struk fisik opsional. |
| 5 | Activity diagram memiliki satu awal dan minimal satu akhir? | **Lolos.** Seluruh activity diagram diawali 1 simpul `Mulai` dan berakhir di `Selesai`. |
| 6 | Setiap keputusan memiliki semua cabang berlabel (Ya/Tidak)? | **Lolos.** Seluruh simpul keputusan `{}` memiliki cabang berlabel jelas. |
| 7 | Pengecualian pada skenario (misal uang kurang/menu habis) muncul di diagram? | **Lolos.** Kondisi gagal tercakup dengan alur kembali (*loop-back*) ke perbaikan input. |
| 8 | Tidak ada aktivitas buntu atau perulangan tanpa jalan keluar? | **Lolos.** Seluruh jalur memiliki titik keluar yang terdefinisi. |
