"""services.py.

Lapisan Logika Bisnis (Business Logic Layer) - KasirWarung.
Berisi validasi input, aturan bisnis kalkulasi, dan aturan data.
Dilarang memproses rendering HTML atau mengakses SQL secara langsung.
"""


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

