"""Uji pertama pytest: memastikan fixture basis data sementara dan validasi services bekerja."""
import services


def test_validasi_menu_dasar():
    """Memastikan fungsi validasi_menu dapat memvalidasi menu dengan masukan valid."""
    form = {
        "nama": "Ayam Goreng Sambal",
        "kategori_id": "1",
        "harga": "18000",
        "status": "tersedia",
    }
    data, galat = services.validasi_menu(form)
    assert galat == []
    assert data["nama"] == "Ayam Goreng Sambal"
    assert data["harga"] == 18000
