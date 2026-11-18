"""Uji Langkah 4 Jobsheet 11: 5 Skenario Login dan Logout Sesi."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app

client = app.app.test_client()

print("=== UJI LANGKAH 4: AUTENTIKASI LOGIN & LOGOUT ===")

# Uji 1: Kata sandi benar (pak_joko / joko12345)
res1 = client.post(
    "/login",
    data={"username": "pak_joko", "password": "joko12345"},
    follow_redirects=True,
)
assert res1.status_code == 200
assert "Selamat datang, Pak Joko" in res1.get_data(as_text=True)
print("  [LULUS] Uji 1: Login dengan kredensial benar berhasil masuk.")

# Uji 2: Kata sandi salah
client.post("/logout")
res2 = client.post(
    "/login",
    data={"username": "pak_joko", "password": "katasandisalah"},
)
assert res2.status_code == 200
assert "Nama pengguna atau kata sandi salah." in res2.get_data(as_text=True)
print("  [LULUS] Uji 2: Kata sandi salah menampilkan pesan galat yang aman.")

# Uji 3: Nama pengguna tidak ada
res3 = client.post(
    "/login",
    data={"username": "user_fiktif_999", "password": "sembarangpassword"},
)
assert res3.status_code == 200
assert "Nama pengguna atau kata sandi salah." in res3.get_data(as_text=True)
print("  [LULUS] Uji 3: Username fiktif menampilkan pesan galat yang sama persis (anti-enumerasi).")

# Uji 4: Open Redirect Protection (next=https://jahat.example)
res4 = client.post(
    "/login?next=https://jahat.example",
    data={"username": "pak_joko", "password": "joko12345"},
    follow_redirects=False,
)
assert res4.status_code == 302
# Harus dialihkan ke /menu, BUKAN ke https://jahat.example
assert "jahat.example" not in res4.headers["Location"]
assert "/menu" in res4.headers["Location"]
print("  [LULUS] Uji 4: Celah Open Redirect ditangkal; dialihkan ke rute internal /menu.")

# Uji 5: Logout melalui POST
res5 = client.post("/logout", follow_redirects=True)
assert res5.status_code == 200
assert "Anda telah berhasil keluar" in res5.get_data(as_text=True)
print("  [LULUS] Uji 5: Logout melalui POST berhasil mengosongkan sesi.")

print(">>> SELURUH 5 UJI LANGKAH 4 LULUS 100% <<<")
