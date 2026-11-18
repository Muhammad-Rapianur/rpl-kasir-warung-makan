import os
import sqlite3
from datetime import date
from flask import Flask, abort, flash, redirect, render_template, request, url_for
import models
import services

app = Flask(__name__)

# Kunci rahasia dibaca dari variabel lingkungan; nilai default hanya untuk pengembangan lokal.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-kasir-warung-2026")

# Inisialisasi basis data SQLite saat aplikasi pertama kali dimuat
models.init_db()


@app.template_filter("rupiah")
def format_rupiah(nilai):
    """Filter Jinja2 untuk memformat angka ke format mata uang Rupiah (contoh: 15000 -> Rp 15.000)."""
    try:
        return f"Rp {int(nilai):,}".replace(",", ".")
    except (ValueError, TypeError):
        return f"Rp {nilai}"


@app.route("/")
def beranda():
    """Rute beranda utama yang mengalihkan langsung ke modul menu."""
    return redirect(url_for("daftar_menu"))


@app.route("/menu")
def daftar_menu():
    """Halaman daftar menu makanan dan minuman dengan pencarian dan filter (Langkah 9 & 10)."""
    kata = request.args.get("q", "").strip()
    kategori_raw = request.args.get("kategori", "").strip()
    status = request.args.get("status", "").strip() or None

    kategori_id = int(kategori_raw) if kategori_raw.isdigit() else None
    daftar = models.cari_menu(kata=kata, kategori_id=kategori_id, status=status)
    daftar_kategori = models.semua_kategori()

    return render_template(
        "menu_list.html",
        menu=daftar,
        kategori=daftar_kategori,
        kata=kata,
        kategori_terpilih=kategori_id,
        status_terpilih=status,
    )


@app.route("/menu/tambah", methods=["GET", "POST"])
def tambah_menu():
    """Form tambah menu baru (Create - Langkah 6)."""
    daftar_kategori = models.semua_kategori()

    if request.method == "POST":
        data, galat = services.validasi_menu(request.form)
        if not galat:
            try:
                models.tambah_menu(data["nama"], data["kategori_id"], data["harga"])
            except sqlite3.IntegrityError:
                galat.append(f"Menu dengan nama '{data['nama']}' sudah terdaftar.")
            else:
                flash(f"Menu '{data['nama']}' berhasil ditambahkan.")
                return redirect(url_for("daftar_menu"))

        return render_template(
            "menu_form.html",
            judul="Tambah Menu Baru",
            menu=request.form,
            kategori=daftar_kategori,
            galat=galat,
            apakah_ubah=False,
        )

    return render_template(
        "menu_form.html",
        judul="Tambah Menu Baru",
        menu={},
        kategori=daftar_kategori,
        galat=[],
        apakah_ubah=False,
    )


@app.route("/menu/<int:menu_id>/ubah", methods=["GET", "POST"])
def ubah_menu(menu_id):
    """Form ubah menu hidangan (Update - Langkah 8)."""
    menu = models.ambil_menu(menu_id)
    if menu is None:
        abort(404)

    daftar_kategori = models.semua_kategori()

    if request.method == "POST":
        data, galat = services.validasi_menu(request.form)
        status = request.form.get("status", "tersedia")
        if status not in ("tersedia", "habis"):
            status = "tersedia"

        if not galat:
            try:
                models.ubah_menu(
                    menu_id,
                    data["nama"],
                    data["kategori_id"],
                    data["harga"],
                    status,
                )
            except sqlite3.IntegrityError:
                galat.append(f"Menu dengan nama '{data['nama']}' sudah terdaftar.")
            else:
                flash(f"Menu '{data['nama']}' berhasil diperbarui.")
                return redirect(url_for("daftar_menu"))

        return render_template(
            "menu_form.html",
            judul="Ubah Menu Hidangan",
            menu=request.form,
            kategori=daftar_kategori,
            galat=galat,
            apakah_ubah=True,
        )

    return render_template(
        "menu_form.html",
        judul="Ubah Menu Hidangan",
        menu=dict(menu),
        kategori=daftar_kategori,
        galat=[],
        apakah_ubah=True,
    )


@app.route("/menu/<int:menu_id>/hapus", methods=["POST"])
def hapus_menu(menu_id):
    """Hapus data menu hidangan (Delete - Langkah 9).

    Hanya menerima metode HTTP POST demi keamanan web.
    """
    menu = models.ambil_menu(menu_id)
    if menu is None:
        abort(404)

    try:
        models.hapus_menu(menu_id)
    except sqlite3.IntegrityError:
        flash(
            f"Menu '{menu['nama']}' tidak dapat dihapus karena sudah memiliki riwayat transaksi penjualan."
        )
    else:
        flash(f"Menu '{menu['nama']}' berhasil dihapus.")

    return redirect(url_for("daftar_menu"))


# ============================================================
# Modul CRUD Entitas Kedua: Kategori (Langkah 14 - PT & BM)
# ============================================================

@app.route("/kategori")
def daftar_kategori():
    """Halaman daftar seluruh kategori hidangan."""
    kategori = models.semua_kategori_detail()
    return render_template("kategori_list.html", kategori=kategori)


@app.route("/kategori/tambah", methods=["GET", "POST"])
def tambah_kategori():
    """Form tambah kategori baru."""
    if request.method == "POST":
        data, galat = services.validasi_kategori(request.form)
        if not galat:
            try:
                models.tambah_kategori(data["nama"])
            except sqlite3.IntegrityError:
                galat.append(f"Kategori '{data['nama']}' sudah terdaftar.")
            else:
                flash(f"Kategori '{data['nama']}' berhasil ditambahkan.")
                return redirect(url_for("daftar_kategori"))

        return render_template(
            "kategori_form.html",
            judul="Tambah Kategori Baru",
            kategori=request.form,
            galat=galat,
        )

    return render_template(
        "kategori_form.html",
        judul="Tambah Kategori Baru",
        kategori={},
        galat=[],
    )


@app.route("/kategori/<int:kategori_id>/ubah", methods=["GET", "POST"])
def ubah_kategori(kategori_id):
    """Form ubah nama kategori."""
    kategori = models.ambil_kategori(kategori_id)
    if kategori is None:
        abort(404)

    if request.method == "POST":
        data, galat = services.validasi_kategori(request.form)
        if not galat:
            try:
                models.ubah_kategori(kategori_id, data["nama"])
            except sqlite3.IntegrityError:
                galat.append(f"Kategori '{data['nama']}' sudah terdaftar.")
            else:
                flash(f"Kategori '{data['nama']}' berhasil diperbarui.")
                return redirect(url_for("daftar_kategori"))

        return render_template(
            "kategori_form.html",
            judul="Ubah Kategori",
            kategori=request.form,
            galat=galat,
        )

    return render_template(
        "kategori_form.html",
        judul="Ubah Kategori",
        kategori=dict(kategori),
        galat=[],
    )


@app.route("/kategori/<int:kategori_id>/hapus", methods=["POST"])
def hapus_kategori(kategori_id):
    """Hapus kategori (hanya POST).

    Menolak penghapusan bila kategori masih dirujuk oleh tabel menu.
    """
    kategori = models.ambil_kategori(kategori_id)
    if kategori is None:
        abort(404)

    try:
        models.hapus_kategori(kategori_id)
    except sqlite3.IntegrityError:
        flash(
            f"Kategori '{kategori['nama']}' tidak dapat dihapus karena masih digunakan oleh menu hidangan."
        )
    else:
        flash(f"Kategori '{kategori['nama']}' berhasil dihapus.")

    return redirect(url_for("daftar_kategori"))


# ============================================================
# Modul Transaksi & Detail Transaksi Berelasi (Jobsheet 10)
# ============================================================

@app.route("/transaksi")
def daftar_transaksi():
    """Halaman riwayat transaksi penjualan (Read dengan JOIN & Agregasi)."""
    daftar = models.semua_transaksi()
    return render_template("transaksi_list.html", transaksi=daftar)


@app.route("/transaksi/tambah", methods=["GET", "POST"])
def tambah_transaksi():
    """Form catat transaksi penjualan baru dengan relasi detail (Langkah 4 & 5)."""
    daftar_menu = models.semua_menu()
    isian_default = {"tanggal": date.today().isoformat(), "jumlah": 1}

    if request.method == "POST":
        data, galat = services.validasi_transaksi(request.form)

        # Validasi menu induk (cek apakah menu_id benar-benar ada)
        menu_pilihan = None
        if data["menu_id"]:
            menu_pilihan = models.ambil_menu(data["menu_id"])
            if menu_pilihan is None:
                galat.append("Menu hidangan tidak ditemukan di database.")

        if not galat:
            try:
                nomor_trx = models.tambah_transaksi_dengan_detail(
                    menu_id=data["menu_id"],
                    jumlah=data["jumlah"],
                    tanggal_waktu=data["tanggal_waktu"],
                    tipe_pesanan=data["tipe_pesanan"],
                    nomor_meja=data["nomor_meja"],
                    metode_pembayaran=data["metode_pembayaran"],
                    uang_diterima=data["uang_diterima"],
                    pengguna_id=2,  # Kasir Utama
                )
            except sqlite3.IntegrityError as err:
                galat.append(f"Gagal mencatat transaksi: {err}")
            else:
                flash(f"Transaksi {nomor_trx} berhasil dicatat.")
                return redirect(url_for("daftar_transaksi"))

        return render_template(
            "transaksi_form.html",
            menu=daftar_menu,
            isian=request.form,
            galat=galat,
        )

    return render_template(
        "transaksi_form.html",
        menu=daftar_menu,
        isian=isian_default,
        galat=[],
    )



if __name__ == "__main__":
    app.run(debug=True)
