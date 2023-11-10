from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db_siswa'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_user")
    data_users = cur.fetchall()
    cur.close()
    return render_template('index.html', data_users=data_users)

@app.route('/tambah_data', methods=['GET', 'POST'])
def tambah_data():
    if request.method == 'POST':
        id = request.form['id']
        nama = request.form['nama']
        alamat = request.form['alamat']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO data_user (id, nama, alamat, email) VALUES (%s, %s, %s, %s)", (id, nama, alamat, email))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    return render_template('tambah_data.html')

@app.route('/edit_data/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_user WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        new_nama = request.form['nama']
        new_alamat = request.form['alamat']
        new_email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE data_user SET nama=%s, alamat=%s, email=%s WHERE id=%s", (new_nama, new_alamat, new_email, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    return render_template('edit_data.html', user=user)

@app.route('/hapus_data/<int:id>')
def hapus_data(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM data_user WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
