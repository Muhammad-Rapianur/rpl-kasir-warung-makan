"""Lapisan Logika Bisnis (Business Logic Layer) - KasirWarung.

Berisi validasi input, aturan bisnis kalkulasi, dan aturan data.
Dilarang memproses rendering HTML atau mengakses SQL secara langsung.
"""
from datetime import date, datetime


def _bilangan_positif(teks):
    """Ubah teks menjadi bilangan bulat positif (> 0), atau None bila tidak valid/negatif/kosong."""
    if teks is None:
        return None
    teks = str(teks).strip()
    if not teks.isdigit():
        return None
    nilai = int(teks)
    return nilai if nilai > 0 else None


def validasi_menu(form):
    """Validasi data form menu (nama, kategori_id, harga).

    Kembalikan tuple (data_bersih, daftar_galat).
    Aturan validasi mengikuti kamus data & SRS:
    - Nama hidangan tidak boleh kosong (minimal 2 karakter).
    - Kategori wajib dipilih.
    - Harga wajib berupa angka positif (> 0).
    """
    galat = []
    nama = (form.get("nama") or "").strip()
    kategori_id = form.get("kategori_id")
    harga_raw = form.get("harga")

    if not nama:
        galat.append("Nama menu hidangan wajib diisi.")
    elif len(nama) < 2:
        galat.append("Nama menu minimal terdiri dari 2 karakter.")

    try:
        kat_id = int(str(kategori_id).strip()) if kategori_id else None
        if not kat_id:
            galat.append("Kategori menu wajib dipilih.")
    except (ValueError, TypeError):
        kat_id = None
        galat.append("Kategori menu tidak valid.")

    harga = _bilangan_positif(harga_raw)
    if harga is None:
        galat.append(
            "Harga jual harus berupa bilangan bulat positif lebih besar dari 0 (contoh: 15000)."
        )

    data_bersih = {
        "nama": nama,
        "kategori_id": kat_id,
        "harga": harga,
    }
    return data_bersih, galat


def validasi_kategori(form):
    """Validasi form tambah/ubah kategori.

    - Nama kategori wajib diisi.
    - Minimal 3 karakter.
    """
    galat = []
    nama = (form.get("nama") or "").strip()

    if not nama:
        galat.append("Nama kategori wajib diisi.")
    elif len(nama) < 3:
        galat.append("Nama kategori minimal 3 karakter.")

    return {"nama": nama}, galat


def validasi_transaksi(form):
    """Validasi form pencatatan transaksi kasir baru (Langkah 4).

    Menguji menu_id, kuantitas, format tanggal, dan metode bayar.
    """
    galat = []

    # 1. Validasi Menu ID (Induk)
    menu_id_raw = form.get("menu_id")
    menu_id = None
    if not menu_id_raw or str(menu_id_raw).strip() == "":
        galat.append("Pilih menu hidangan.")
    else:
        try:
            menu_id = int(str(menu_id_raw).strip())
        except (ValueError, TypeError):
            galat.append("Pilihan menu tidak valid.")

    # 2. Validasi Jumlah (harus bilangan bulat > 0)
    jumlah_raw = form.get("jumlah")
    jumlah = None
    if not jumlah_raw or str(jumlah_raw).strip() == "":
        galat.append("Jumlah porsi harus berupa angka lebih dari 0.")
    else:
        teks_jml = str(jumlah_raw).strip()
        if not teks_jml.isdigit() or int(teks_jml) <= 0:
            galat.append("Jumlah porsi harus berupa angka lebih dari 0.")
        else:
            jumlah = int(teks_jml)

    # 3. Validasi Tanggal (Wajib format TTTT-BB-HH / ISO)
    tanggal_raw = (form.get("tanggal") or "").strip()
    if not tanggal_raw:
        galat.append("Tanggal transaksi wajib diisi.")
        tanggal_iso = date.today().isoformat()
    else:
        try:
            # Uji format TTTT-BB-HH (ISO)
            parsed_date = date.fromisoformat(tanggal_raw)
            # Simpan dengan jam saat ini
            waktu_sekarang = datetime.now().strftime("%H:%M:%S")
            tanggal_iso = f"{parsed_date.isoformat()} {waktu_sekarang}"
        except ValueError:
            galat.append("Tanggal harus berformat TTTT-BB-HH (contoh: 2026-11-19).")
            tanggal_iso = None

    # 4. Validasi Tipe Pesanan
    tipe_pesanan = form.get("tipe_pesanan", "dine_in")
    if tipe_pesanan not in ("dine_in", "take_away"):
        tipe_pesanan = "dine_in"

    nomor_meja = (form.get("nomor_meja") or "").strip() or None
    if tipe_pesanan == "dine_in" and not nomor_meja:
        nomor_meja = "01"  # Default nomor meja jika tidak diisi

    # 5. Validasi Metode Bayar & Uang Diterima
    metode_pembayaran = form.get("metode_pembayaran", "tunai")
    if metode_pembayaran not in ("tunai", "qris"):
        metode_pembayaran = "tunai"

    uang_raw = form.get("uang_diterima", "0")
    try:
        uang_diterima = int(str(uang_raw).strip()) if str(uang_raw).strip().isdigit() else 0
    except (ValueError, TypeError):
        uang_diterima = 0

    data = {
        "menu_id": menu_id,
        "jumlah": jumlah,
        "tanggal_waktu": tanggal_iso,
        "tipe_pesanan": tipe_pesanan,
        "nomor_meja": nomor_meja,
        "metode_pembayaran": metode_pembayaran,
        "uang_diterima": uang_diterima,
    }
    return data, galat


