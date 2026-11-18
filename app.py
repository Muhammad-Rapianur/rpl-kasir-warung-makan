import os
from flask import Flask, redirect, render_template, url_for
import models

app = Flask(__name__)

# Kunci rahasia dibaca dari variabel lingkungan; nilai default hanya untuk pengembangan lokal.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-kasir-warung-2026")

# Inisialisasi basis data SQLite saat aplikasi pertama kali dimuat
models.init_db()


@app.route("/")
def beranda():
    """Rute beranda utama yang mengalihkan langsung ke modul menu."""
    return redirect(url_for("daftar_menu"))


@app.route("/menu")
def daftar_menu():
    """Halaman daftar menu makanan dan minuman (Read - Langkah 5)."""
    daftar = models.semua_menu()
    return render_template("menu_list.html", menu=daftar)


if __name__ == "__main__":
    app.run(debug=True)
