import os
import sqlite3
from datetime import date
from functools import wraps
from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
import models
import services

app = Flask(__name__)

# Kunci rahasia dibaca dari variabel lingkungan; nilai default hanya untuk pengembangan lokal.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-kasir-warung-2026")

# Konfigurasi keamanan cookie sesi Flask (Jobsheet 11 - H2)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

# Inisialisasi basis data SQLite saat aplikasi pertama kali dimuat
models.init_db()


def _tujuan_aman(tujuan):
    """Mencegah serangan Open Redirect: hanya menerima path internal dalam situs."""
    if tujuan and tujuan.startswith("/") and not tujuan.startswith("//") and "\\" not in tujuan:
        return tujuan
    return None


@app.before_request
def muat_pengguna():
    """Memuat data g.pengguna dari basis data berdasarkan session pengguna_id pada setiap request."""
    pengguna_id = session.get("pengguna_id")
    g.pengguna = models.ambil_pengguna(pengguna_id) if pengguna_id else None


def peran_diperlukan(*peran):
    """Batasi rute: belum masuk -> dialihkan ke /login?next=...; peran tidak cocok -> 403 (Jobsheet 11 - H3)."""
    def dekorator(fungsi):
        @wraps(fungsi)
        def bungkus(*args, **kwargs):
            if g.pengguna is None:
                # Tamu diarahkan ke login membawa parameter next
                return redirect(url_for("login", next=request.full_path.rstrip("?")))
            if g.pengguna["peran"] not in peran:
                # Peran tidak berhak ditolak dengan 403 Forbidden
                abort(403)
            return fungsi(*args, **kwargs)
        return bungkus
    return dekorator


semua_peran = peran_diperlukan(*services.PERAN)
hanya_pemilik = peran_diperlukan("pemilik")


@app.errorhandler(403)
def akses_dilarang(_galat):
    """Menampilkan halaman 403 yang ramah pengguna jika hak akses peran tidak terpenuhi."""
    return render_template("403.html"), 403


@app.template_filter("rupiah")
def format_rupiah(nilai):
    """Filter Jinja2 untuk memformat angka ke format mata uang Rupiah (contoh: 15000 -> Rp 15.000)."""
    try:
        return f"Rp {int(nilai):,}".replace(",", ".")
    except (ValueError, TypeError):
        return f"Rp {nilai}"


@app.route("/login", methods=["GET", "POST"])
def login():
    """Halaman dan proses autentikasi login (Jobsheet 11 - Fitur H2)."""
    if g.pengguna:
        return redirect(url_for("daftar_menu"))

    galat = []
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        pengguna = services.autentikasi(username, password)
        if pengguna:
            session.clear()  # Regenerasi sesi (cegah session fixation)
            session["pengguna_id"] = pengguna["id"]
            flash(f"Selamat datang, {pengguna['nama_lengkap']}!")
            tujuan = _tujuan_aman(request.args.get("next"))
            return redirect(tujuan or url_for("daftar_menu"))

        # Satu pesan umum untuk mencegah kebocoran keberadaan username
        galat.append("Nama pengguna atau kata sandi salah.")

    return render_template(
        "login.html",
        galat=galat,
        username=request.form.get("username", ""),
    )


@app.route("/logout", methods=["POST"])
def logout():
    """Proses keluar akun yang aman: hanya menerima metode POST (Jobsheet 11 - H2)."""
    session.clear()
    flash("Anda telah berhasil keluar dari sistem kasir.")
    return redirect(url_for("login"))


@app.route("/")
@semua_peran
def beranda():
    """Rute beranda utama yang mengalihkan langsung ke modul menu."""
    return redirect(url_for("daftar_menu"))


@app.route("/menu")
@semua_peran
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


def _render_menu_form(judul, menu, kategori, galat=None, apakah_ubah=False):
    """Fungsi bantu hasil refactoring untuk merender form menu tanpa duplikasi (Langkah 13)."""
    return render_template(
        "menu_form.html",
        judul=judul,
        menu=menu,
        kategori=kategori,
        galat=galat or [],
        apakah_ubah=apakah_ubah,
    )


@app.route("/menu/tambah", methods=["GET", "POST"])
@hanya_pemilik
def tambah_menu():
    """Form tambah menu baru (Create - Hanya Pemilik)."""
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

        return _render_menu_form("Tambah Menu Baru", request.form, daftar_kategori, galat, False)

    return _render_menu_form("Tambah Menu Baru", {}, daftar_kategori, [], False)


@app.route("/menu/<int:menu_id>/ubah", methods=["GET", "POST"])
@hanya_pemilik
def ubah_menu(menu_id):
    """Form ubah menu hidangan (Update - Hanya Pemilik)."""
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

        return _render_menu_form("Ubah Menu Hidangan", request.form, daftar_kategori, galat, True)

    return _render_menu_form("Ubah Menu Hidangan", dict(menu), daftar_kategori, [], True)


@app.route("/menu/<int:menu_id>/hapus", methods=["POST"])
@hanya_pemilik
def hapus_menu(menu_id):
    """Hapus data menu hidangan (Delete - Hanya Pemilik).

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
# Modul CRUD Entitas Kedua: Kategori (Hanya Pemilik)
# ============================================================

@app.route("/kategori")
@hanya_pemilik
def daftar_kategori():
    """Halaman daftar seluruh kategori hidangan."""
    kategori = models.semua_kategori_detail()
    return render_template("kategori_list.html", kategori=kategori)


@app.route("/kategori/tambah", methods=["GET", "POST"])
@hanya_pemilik
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
@hanya_pemilik
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
@hanya_pemilik
def hapus_kategori(kategori_id):
    """Hapus kategori (hanya POST - Hanya Pemilik)."""
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
# Modul Transaksi & Detail Transaksi (Semua Peran: Kasir & Pemilik)
# ============================================================

@app.route("/transaksi")
@semua_peran
def daftar_transaksi():
    """Halaman riwayat transaksi penjualan (Read dengan JOIN & Agregasi)."""
    daftar = models.semua_transaksi()
    return render_template("transaksi_list.html", transaksi=daftar)


@app.route("/transaksi/tambah", methods=["GET", "POST"])
@semua_peran
def tambah_transaksi():
    """Form catat transaksi penjualan baru dengan relasi detail (Semua Peran)."""
    daftar_menu = models.semua_menu()
    isian_default = {"tanggal": date.today().isoformat(), "jumlah": 1}

    if request.method == "POST":
        data, galat = services.validasi_transaksi(request.form)

        menu_pilihan = None
        if data["menu_id"]:
            menu_pilihan = models.ambil_menu(data["menu_id"])
            if menu_pilihan is None:
                galat.append("Menu hidangan tidak ditemukan di database.")

        if not galat:
            try:
                # Gunakan ID pengguna yang sedang login di sesi
                kasir_id = g.pengguna["id"] if g.pengguna else 2
                nomor_trx = models.tambah_transaksi_dengan_detail(
                    menu_id=data["menu_id"],
                    jumlah=data["jumlah"],
                    tanggal_waktu=data["tanggal_waktu"],
                    tipe_pesanan=data["tipe_pesanan"],
                    nomor_meja=data["nomor_meja"],
                    metode_pembayaran=data["metode_pembayaran"],
                    uang_diterima=data["uang_diterima"],
                    pengguna_id=kasir_id,
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
