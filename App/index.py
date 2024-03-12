from flask_sqlalchemy import SQLAlchemy, session
import mysql.connector
from flask_mysqldb import MySQL
from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin
import secrets
from App.models import HocSinh, User, Lop, Diem

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Diemhang662'
app.config['MYSQL_DB'] = 'quanlyhocsinh'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Diemhang662@localhost/quanlyhocsinh?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

my_sql = MySQL(app)
mysql = mysql.connector.connect(user="root", password="Diemhang662", database="quanlyhocsinh")


@app.route("/")
def index():
    return render_template('index.html')


class TaiKhoan(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    with app.app_context():
        db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
     msg=' '
     if request.method == 'POST':
        cur = my_sql.connection.cursor()
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute('SELECT * FROM tai_khoan WHERE email=%s AND password=%s',(email, password))
        record = cur.fetchone()
        if record:
            session['loggedin']=True
            session['email'] = record[1]
            return redirect(url_for('index_1'))
        else:
            msg=''

     return render_template('login.html', msg=msg)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/index_1')
def index_1():
    return render_template('index_1.html')


@app.route('/QLHS')
def QLHS():
    hs = db.session.query(HocSinh)
    return render_template('QLHS.html', hs=hs)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        HoTen = request.form['HoTen']
        NgaySinh = request.form['NgaySinh']
        GioiTinh = request.form['GioiTinh']
        DiaChi = request.form['DiaChi']
        SDT = request.form['SDT']
        Email = request.form['Email']

        cur = mysql.cursor()
        cur.execute( "INSERT INTO hoc_sinh (HoTen, NgaySinh, GioiTinh, DiaChi, SDT, Email) VALUES (%s, %s, %s, %s, %s, %s)",
        (HoTen, NgaySinh, GioiTinh, DiaChi, SDT, Email))
        mysql.commit()
        cur.close()
        return redirect(url_for('QLHS'))


@app.route('/delete/<string:ten>', methods=['GET'])
def delete(ten):
    cur = my_sql.connection.cursor()
    cur.execute("DELETE FROM hoc_sinh WHERE HoTen=%s", (ten,))
    my_sql.connection.commit()
    return redirect(url_for('QLHS'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ten = request.form['HoTen']
        hs = search_students_by_name(ten)
        return render_template('QLHS.html', hs=hs)
    return redirect(url_for('index_1'))

def search_students_by_name(ten):
    try:
        cur = my_sql.connection.cursor()
        cur.execute("SELECT * FROM hoc_sinh WHERE HoTen LIKE %s", ('%' + ten + '%',))
        hs = cur.fetchall()
        return hs
    except Exception as e:
        return str(e)
    finally:
        cur.close()

@app.route('/QLLop')
def QLLop():
    lop = db.session.query(Lop)
    return render_template('QLLop.html', lop=lop)

@app.route('/SearchClass', methods=['GET', 'POST'])
def SearchClass():
    if request.method == 'POST':
        TenLop = request.form['TenLop']
        hs = SearchClassByName(TenLop)
        return render_template('QLLop.html', hs=hs, TenLop=TenLop)
    return redirect(url_for('index_1'))

def SearchClassByName(TenLop):
    cur = my_sql.connection.cursor()
    cur.execute (f"SELECT * FROM hoc_sinh hs JOIN lop l ON hs.Lop_id = l.MaLop WHERE l.TenLop = '{TenLop}'")
    hs = cur.fetchall()
    return hs



@app.route('/QLDiem', methods=['GET', 'POST'])
def QLDiem():
    if request.method == 'POST':
        MaHS = request.form.get('MaHS')
        if MaHS:
            return redirect(url_for('QLDiemChiTiet', MaHS=int(MaHS)))

    return render_template('QLDiem.html', hs=None, diems=None)

@app.route('/QLDiem/<int:MaHS>')
def QLDiemChiTiet(MaHS):
    hs = HocSinh.query.get(MaHS)
    if hs:
        app.logger.info( f"SQL Query: {Diem.query.filter_by(HocSinh_id=MaHS).all()}")
        diems = Diem.query.filter_by(HocSinh_id=MaHS).all()
        return render_template('QLDiem.html', hs=hs, diems=diems)
    else:
        return render_template('QLDiem.html', hs=None, diems=None)

#@app.route('/bao-cao-tong-ket/<int:nam_hoc>/<int:hoc_ky>')
# def bao_cao_tong_ket(nam_hoc, hoc_ky):
    # Lấy dữ liệu từ database (chưa sử dụng ORM)
    # cursor = mysql.cursor(dictionary=True)
    # cursor.execute("""
    #     SELECT mon_hoc.TenMH, COUNT(diem.MaDiem) as SoLuong,
    #     AVG(diem15p.DiemL1 + diem15p.DiemL2 + diem1t.Diem1T + diem_thi.DiemThi) as TyLe
    #     FROM diem
    #     JOIN mon_hoc ON diem.MonHoc_id = mon_hoc.MaMH
    #     JOIN hoc_ky ON diem.HocKy_id = hoc_ky.MaHK
    #     LEFT JOIN diem15p ON diem.MaDiem = diem15p.Diem_id
    #     LEFT JOIN diem1t ON diem.MaDiem = diem1t.Diem_id
    #     LEFT JOIN diem_thi ON diem.MaDiem = diem_thi.Diem_id
   #    WHERE hoc_ky.NamHoc = %s AND hoc_ky.MaHK = %s
        # GROUP BY mon_hoc.TenMH
    # """, (nam_hoc, hoc_ky))
  # result = cursor.fetchall()
  #  cursor.close()

   # return render_template('bao_cao_tong_ket.html', nam_hoc=nam_hoc, hoc_ky=hoc_ky, bao_cao=result)





@app.route('/bao_cao_tong_ket')
def bao_cao_tong_ket():
   # diem = db.session.query(Diem)
    return render_template('bao_cao_tong_ket.html')
if __name__ == "__main__":
    app.run(debug=True)