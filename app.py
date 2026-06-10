from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

# Lokasi folder project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Inisialisasi Flask
application = Flask(__name__)

# Lokasi database SQLite
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS buku (
        id TEXT PRIMARY KEY,
        judul TEXT NOT NULL,
        penulis TEXT NOT NULL,
        penerbit TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# Buat tabel otomatis saat aplikasi dijalankan
init_db()


@application.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM buku")
    container = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        container=container
    )


@application.route("/tambah", methods=["GET", "POST"])
def tambah():

    if request.method == "POST":

        id_buku = request.form["id"]
        judul = request.form["judul"]
        penulis = request.form["penulis"]
        penerbit = request.form["penerbit"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO buku
            (id, judul, penulis, penerbit)
            VALUES (?, ?, ?, ?)
            """,
            (id_buku, judul, penulis, penerbit)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("tambah_form.html")


@application.route("/ubah/<id>", methods=["GET", "POST"])
def ubah(id):

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        judul = request.form["judul"]
        penulis = request.form["penulis"]
        penerbit = request.form["penerbit"]

        cursor.execute(
            """
            UPDATE buku
            SET judul = ?,
                penulis = ?,
                penerbit = ?
            WHERE id = ?
            """,
            (judul, penulis, penerbit, id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM buku WHERE id = ?",
        (id,)
    )

    buku = cursor.fetchone()

    conn.close()

    return render_template(
        "ubah_form.html",
        buku=buku
    )


@application.route("/hapus/<id>")
def hapus(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM buku WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@application.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    print("PORT =", port)

    application.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
