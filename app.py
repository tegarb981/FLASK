from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(BASE_DIR, 'vendor')
if os.path.exists(VENDOR_DIR) and VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

application = Flask(__name__)
application.config['DB_NAME'] = os.path.join(BASE_DIR, 'database.db')

conn = cursor = None

def openDb():
    global conn, cursor
    conn = sqlite3.connect(application.config['DB_NAME'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

def closeDb():
    global conn, cursor
    if cursor: cursor.close()
    if conn: conn.close()

@application.route('/')
def index():
    openDb()
    cursor.execute('SELECT * FROM buku')
    container = cursor.fetchall()
    closeDb()
    return render_template('index.html', container=container)

@application.route('/tambah', methods=['GET','POST'])
def tambah():
    if request.method == 'POST':
        id = request.form['id']
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        data = (id, judul, penulis, penerbit)
        openDb()
        cursor.execute('INSERT INTO buku VALUES(?,?,?,?)', data)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        return render_template('tambah_form.html')

@application.route('/ubah/<id>', methods=['GET','POST'])
def ubah(id):
    openDb()
    if request.method == 'POST':
        judul = request.form['judul']
        penulis = request.form['penulis']
        penerbit = request.form['penerbit']
        cursor.execute('''
            UPDATE buku SET judul=?, penulis=?, penerbit=?
            WHERE id=?
        ''', (judul, penulis, penerbit, id))
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        cursor.execute('SELECT * FROM buku WHERE id=?', (id,))
        data = cursor.fetchone()
        closeDb()
        return render_template('ubah_form.html', buku=data)

@application.route('/hapus/<id>', methods=['GET','POST'])
def hapus(id):
    openDb()
    cursor.execute('DELETE FROM buku WHERE id=?', (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)