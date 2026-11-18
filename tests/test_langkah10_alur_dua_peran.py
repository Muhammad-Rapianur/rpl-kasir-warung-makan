"""Uji Langkah 10 Jobsheet 11: Uji Alur Integrasi Penuh Dua Peran (Lampiran D.1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app

client = app.app.test_client()

print("=== UJI LANGKAH 10: ALUR INTEGRASI DUA PERAN (PEMILIK & KASIR) ===")

# 1. Buka alamat utama tanpa login -> dialihkan ke login
res1 = client.get("/", follow_redirects=False)
assert res1.status_code == 302
assert "/login" in res1.headers["Location"]
print("  [LULUS] Langkah 1: Akses anonim dialihkan ke /login.")

# 2. Masuk sebagai peran penuh (Pemilik: pak_joko)
res2 = client.post("/login", data={"username": "pak_joko", "password": "joko12345"}, follow_redirects=True)
assert res2.status_code == 200
html2 = res2.get_data(as_text=True)
assert "Pak Joko" in html2
assert "Kelola Kategori" in html2
assert "+ Tambah Menu Baru" in html2
print("  [LULUS] Langkah 2: Pemilik berhasil masuk dengan menu navigasi manajerial lengkap.")

# 3. Pemilik menambah satu menu baru
res3 = client.post(
    "/menu/tambah",
    data={"nama": "Soto Banjar Spesial", "kategori_id": "1", "harga": "22000"},
    follow_redirects=True,
)
assert res3.status_code == 200
assert "berhasil ditambahkan" in res3.get_data(as_text=True)
print("  [LULUS] Langkah 3: Pemilik berhasil menambah menu baru.")

# 4. Pemilik mencatat transaksi penjualan
res4 = client.post(
    "/transaksi/tambah",
    data={
        "menu_id": "1",
        "jumlah": "2",
        "tanggal": "2026-11-19",
        "tipe_pesanan": "dine_in",
        "nomor_meja": "11",
        "metode_pembayaran": "tunai",
        "uang_diterima": "50000",
    },
    follow_redirects=True,
)
assert res4.status_code == 200
assert "berhasil dicatat" in res4.get_data(as_text=True)
print("  [LULUS] Langkah 4: Transaksi berhasil dicatat dan tampil di riwayat.")

# 5. Keluar (Logout)
res5 = client.post("/logout", follow_redirects=True)
assert res5.status_code == 200
assert "Anda telah berhasil keluar" in res5.get_data(as_text=True)
print("  [LULUS] Langkah 5: Logout berhasil mengosongkan sesi.")

# 6. Masuk sebagai peran terbatas (Kasir: siti_kasir)
res6 = client.post("/login", data={"username": "siti_kasir", "password": "siti12345"}, follow_redirects=True)
assert res6.status_code == 200
html6 = res6.get_data(as_text=True)
assert "siti_kasir" in html6
assert "Kelola Kategori" not in html6  # Menu manajerial disembunyikan
assert "+ Tambah Menu Baru" not in html6
print("  [LULUS] Langkah 6: Kasir masuk dengan tampilan antarmuka katalog yang bersih.")

# 7. Kasir nekat mengetik URL tambah menu secara langsung -> 403 Forbidden
res7 = client.get("/menu/tambah")
assert res7.status_code == 403
assert "Akses Ditolak" in res7.get_data(as_text=True)
print("  [LULUS] Langkah 7: Percobaan akses langsung kasir ke /menu/tambah diblokir 403.")

# 8. Kasir mengirim POST hapus menu secara langsung -> 403 Forbidden
res8 = client.post("/menu/1/hapus")
assert res8.status_code == 403
print("  [LULUS] Langkah 8: Percobaan POST hapus dari kasir diblokir 403 di server.")

print("\n>>> SELURUH ALUR INTEGRASI DUA PERAN (8 LANGKAH) LULUS 100% <<<")
