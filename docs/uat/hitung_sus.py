"""Hitung skor SUS (System Usability Scale) untuk KasirWarung v1.0.0.
Jalankan: python docs/uat/hitung_sus.py

Pernyataan SUS (1-5):
1. Merasa akan sering menggunakan sistem ini
2. Merasa sistem terlalu rumit tanpa perlu
3. Merasa sistem mudah digunakan
4. Merasa memerlukan bantuan teknisi untuk menggunakannya
5. Merasa fungsi-fungsi terpadu dengan baik
6. Merasa banyak ketidakkonsistenan
7. Merasa kebanyakan orang belajar memakainya dengan cepat
8. Merasa sangat merepotkan untuk digunakan
9. Merasa sangat percaya diri saat menggunakan
10. Perlu belajar banyak hal sebelum dapat mulai menggunakannya
"""

JAWABAN = {
    "Pemilik Warung": [4, 2, 5, 1, 4, 2, 5, 1, 5, 2],
    "Kasir":          [5, 1, 5, 1, 5, 1, 5, 1, 4, 1],
}


def skor_sus(j):
    """Menghitung nilai SUS dari 10 jawaban (1-5).
    Butir ganjil (1,3,5,7,9): skor = jawaban - 1
    Butir genap (2,4,6,8,10): skor = 5 - jawaban
    Total skor dikalikan 2.5 sehingga berskala 0-100.
    """
    assert len(j) == 10 and all(1 <= x <= 5 for x in j), "Harus 10 jawaban bernilai 1-5"
    jumlah = sum((x - 1) if i % 2 == 0 else (5 - x) for i, x in enumerate(j))
    return jumlah * 2.5


if __name__ == "__main__":
    print("=== PERHITUNGAN SKOR USABILITY SCALE (SUS) KASIRWARUNG ===")
    skor = {nama: skor_sus(j) for nama, j in JAWABAN.items()}
    for nama, s in skor.items():
        print(f"Responden {nama:15s} : {s:5.1f} / 100")
    rata_rata = sum(skor.values()) / len(skor)
    print("-" * 45)
    print(f"Skor Rata-rata SUS      : {rata_rata:5.1f} / 100")
    print(f"Kategori Usability      : {'Sangat Baik (Acceptable / Grade A)' if rata_rata >= 80 else 'Baik'}")
