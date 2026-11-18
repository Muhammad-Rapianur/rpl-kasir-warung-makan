"""Uji Langkah 9 & 10: Pencarian dan Penyaringan Aman (LIKE ? ESCAPE '\\')."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import app
import models

client = app.app.test_client()

print("=== UJI LANGKAH 9 & 10: PENCARIAN DAN PENYARINGAN ===")

# 1. Sebagian nama, case-insensitive
res1 = client.get("/menu?q=ayam")
html1 = res1.get_data(as_text=True)
assert "Ayam Goreng" in html1 or "Ayam Bakar" in html1
assert res1.status_code == 200
print("  [LULUS] Uji 1: Pencarian sebagian nama 'ayam' berhasil menampilkan menu terkait.")

# 2. Kata yang tidak ada
res2 = client.get("/menu?q=PizzaSuperKeju")
html2 = res2.get_data(as_text=True)
assert "Tidak ada menu hidangan yang cocok" in html2
print("  [LULUS] Uji 2: Kata tidak ada menampilkan pesan ramah 'Tidak ada menu yang cocok'.")

# 3. Karakter khusus % atau _
res3 = client.get("/menu?q=%25")
html3 = res3.get_data(as_text=True)
# Karena tidak ada nama hidangan berkarakter '%', harusnya tidak mencocokkan semua baris secara liar
assert "Tidak ada menu hidangan yang cocok" in html3
print("  [LULUS] Uji 3: Karakter wildcard '%' dinetralkan via ESCAPE '\\\\'.")

# 4. Injeksi SQL ' OR 1=1 --
res4 = client.get("/menu?q=' OR 1=1 --")
assert res4.status_code == 200
html4 = res4.get_data(as_text=True)
assert "Tidak ada menu hidangan yang cocok" in html4
print("  [LULUS] Uji 4: Payload SQL Injection dinetralkan via parameter ?.")

# 5. Gabungan pencarian dan filter kategori / status (Langkah 10)
res5 = client.get("/menu?q=ayam&status=tersedia")
assert res5.status_code == 200
html5 = res5.get_data(as_text=True)
assert "Ayam" in html5
print("  [LULUS] Uji 5: Pencarian dan penyaringan berhasil digabungkan (?q=ayam&status=tersedia).")

print(">>> SELURUH UJI LANGKAH 9 & 10 LULUS 100% <<<")
