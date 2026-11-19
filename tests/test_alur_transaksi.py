"""Uji Alur Bisnis (Integration Testing) Sistem Kasir Warung Makan melalui HTTP.
Berkas: tests/test_alur_transaksi.py
Sesuai Jobsheet 13 Langkah 9 dan Lampiran D.3 & D.5.
"""
import models


def test_tambah_menu_lalu_tampil_di_katalog(pemilik, kirim):
    """Alur pemilik menambah menu baru hingga tampil di katalog daftar menu."""
    respon = kirim(
        pemilik,
        "/menu/tambah",
        nama="Nasi Liwet Komplit",
        kategori_id="1",
        harga="28000",
        status="tersedia",
    )
    assert respon.status_code == 200
    assert "Nasi Liwet Komplit" in respon.text
    assert "berhasil" in respon.text.lower()


def test_kasir_catat_transaksi_penjualan(kasir, pemilik, kirim):
    """Alur kasir mencatat pesanan penjualan makanan, menghitung total, dan menerbitkan nomor transaksi."""
    # 1. Pemilik memastikan menu tersedia
    kirim(
        pemilik,
        "/menu/tambah",
        nama="Ayam Bakar Taliwang",
        kategori_id="1",
        harga="25000",
        status="tersedia",
    )
    daftar_menu = models.semua_menu()
    menu_target = [m for m in daftar_menu if m["nama"] == "Ayam Bakar Taliwang"][0]

    # 2. Kasir mencatat transaksi pesanan 2 porsi
    respon_trx = kirim(
        kasir,
        "/transaksi/tambah",
        menu_id=str(menu_target["id"]),
        jumlah="2",
        tanggal="2026-11-20",
        tipe_pesanan="dine_in",
        nomor_meja="07",
        metode_pembayaran="tunai",
        uang_diterima="60000",
    )
    assert respon_trx.status_code == 200
    assert "berhasil dicatat" in respon_trx.text

    # 3. Verifikasi transaksi tersimpan di database dengan relasi lengkap
    semua_trx = models.semua_transaksi()
    assert len(semua_trx) >= 1
    trx_terbaru = semua_trx[0]
    assert trx_terbaru["nomor_transaksi"].startswith("TRX-")
    assert trx_terbaru["total_belanja"] == 50000  # 2 porsi x 25.000
    assert "Ayam Bakar Taliwang" in trx_terbaru["rincian_menu"]


def test_transaksi_porsi_nol_ditolak_lewat_http(kasir, pemilik, kirim):
    """Pencatatan transaksi dengan kuantitas porsi 0 wajib ditolak dengan pesan peringatan."""
    daftar_menu = models.semua_menu()
    menu_id = str(daftar_menu[0]["id"]) if daftar_menu else "1"

    respon = kirim(
        kasir,
        "/transaksi/tambah",
        menu_id=menu_id,
        jumlah="0",
        tanggal="2026-11-20",
        tipe_pesanan="take_away",
        metode_pembayaran="tunai",
        uang_diterima="20000",
    )
    assert "Jumlah porsi harus berupa angka lebih dari 0" in respon.text


def test_hapus_menu_yang_sudah_memiliki_transaksi_ditolak(kasir, pemilik, kirim):
    """Menu yang sudah pernah memiliki riwayat transaksi tidak boleh dihapus (menjaga integritas foreign key)."""
    # Buat menu khusus
    kirim(pemilik, "/menu/tambah", nama="Bebek Goreng Madura", kategori_id="1", harga="35000", status="tersedia")
    menu = [m for m in models.semua_menu() if m["nama"] == "Bebek Goreng Madura"][0]

    # Catat transaksi menggunakan menu tersebut
    kirim(
        kasir,
        "/transaksi/tambah",
        menu_id=str(menu["id"]),
        jumlah="1",
        tanggal="2026-11-20",
        tipe_pesanan="dine_in",
        nomor_meja="03",
        metode_pembayaran="tunai",
        uang_diterima="50000",
    )

    # Pemilik mencoba menghapus menu tersebut
    respon_hapus = kirim(pemilik, f"/menu/{menu['id']}/hapus")
    assert "tidak dapat dihapus" in respon_hapus.text.lower() or "gagal" in respon_hapus.text.lower()

    # Pastikan menu masih tetap ada di database
    menu_cek = models.ambil_menu(menu["id"])
    assert menu_cek is not None, "Menu tidak boleh terhapus karena terikat relasi foreign key"


def test_pencarian_menu_karakter_wildcard_persen_aman(pemilik, kirim):
    """Pencarian menu dengan karakter '%' atau '_' tidak boleh memicu SQL injection dan dianggap huruf biasa."""
    kirim(pemilik, "/menu/tambah", nama="Promo Es Jeruk 100%", kategori_id="1", harga="5000", status="tersedia")
    kirim(pemilik, "/menu/tambah", nama="Es Teh Manis", kategori_id="1", harga="4000", status="tersedia")

    hasil = models.cari_menu(kata="%")
    nama_ditemukan = [m["nama"] for m in hasil]
    assert "Promo Es Jeruk 100%" in nama_ditemukan
    assert "Es Teh Manis" not in nama_ditemukan
