from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask_mysqldb import MySQL
from flask_login import UserMixin, LoginManager

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Diemhang662'
app.config['MYSQL_DB'] = 'quanlyhocsinh'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Diemhang662@localhost/quanlyhocsinh?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app=app)
my_sql = MySQL(app)
mysql = mysql.connector.connect(user="root", password="Diemhang662", database="quanlyhocsinh")


class TaiKhoan(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    with app.app_context():
        db.create_all()

class GiaoVien(db.Model):
    MaGV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    HoTen = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.String(100), nullable=False)
    GioiTinh = db.Column(db.String(10), nullable=False)
    DiaChi = db.Column(db.String(255), nullable=False)
    SDT = db.Column(db.String(13), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    lops = db.relationship('Lop', backref='giao_vien', lazy=True)
    TaiKhoan_id = db.Column(db.Integer, db.ForeignKey('tai_khoan.id'))
    tai_khoan = db.relationship('TaiKhoan', backref=db.backref('giao_vien', lazy=True))

    def __init__(self, HoTen):
        self.HoTen = HoTen

class BaoCaoThongKe(db.Model):
    MaBCTK = db.Column(db.Integer, primary_key=True)
    SLDat = db.column(db.Integer)
    TyLe = db.column(db.Float)
    Lop_id = db.Column(db.Integer, db.ForeignKey('lop.MaLop'))
    MonHoc_id = db.Column(db.Integer, db.ForeignKey('mon_hoc.MaMH'))
    HocKy_id = db.Column(db.Integer, db.ForeignKey('hoc_ky.MaHK'))


class HocSinh(db.Model):
    MaHS = db.Column(db.Integer, primary_key=True,autoincrement=True)
    HoTen = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.String(100), nullable=False)
    GioiTinh = db.Column(db.String(10), nullable=False)
    DiaChi = db.Column(db.String(255), nullable=False)
    SDT = db.Column(db.String(13), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Lop_id = db.Column(db.Integer, db.ForeignKey('lop.MaLop'))
    diems = db.relationship('Diem', backref='hoc_sinh', lazy=True)

    def __init__(self, HoTen, NgaySinh, GioiTinh, DiaChi, SDT, Email, Lop_id):
        self.HoTen = HoTen
        self.NgaySinh = NgaySinh
        self.GioiTinh = GioiTinh
        self.DiaChi = DiaChi
        self.SDT = SDT
        self.Email = Email
        self.Lop_id = Lop_id

class Lop(db.Model):
    MaLop = db.Column(db.Integer, primary_key=True)
    TenLop = db.Column(db.String(100), nullable=False)
    SiSo = db.Column(db.Integer, nullable=False)
    hocsinhs = db.relationship('HocSinh', backref='lop', lazy=True)
    GiaoVien_id = db.Column(db.Integer, db.ForeignKey('giao_vien.MaGV'))
    bctks = db.relationship('BaoCaoThongKe', backref='lop', lazy=True)

    def __init__(self, TenLop, SiSo):
        self.TenLop = TenLop
        self.SiSo = SiSo


class Diem15P(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DiemL1 = db.Column(db.Float, nullable=False )
    DiemL2 = db.Column(db.Float, nullable=False)
    Diem_id = db.Column(db.Integer, db.ForeignKey('diem.MaDiem'))

    def __init__(self, DiemL1, DiemL2, Diem_id):
        self.DiemL1=DiemL1
        self.DiemL2 = DiemL2
        self.Diem_id = Diem_id
class Diem1T(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Diem1T = db.Column(db.Float, nullable=False)
    Diem_id = db.Column(db.Integer, db.ForeignKey('diem.MaDiem'))

    def __init__(self, Diem1T, Diem_id):
        self.Diem1T=Diem1T
        self.Diem_id = Diem_id

class DiemThi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DiemThi = db.Column(db.Float, nullable=False)
    Diem_id = db.Column(db.Integer, db.ForeignKey('diem.MaDiem'))

    def __init__(self, DiemThi, Diem_id):
        self.DiemThi = DiemThi
        self.Diem_id = Diem_id

class HocKy(db.Model):
    MaHK = db.Column(db.Integer, primary_key=True)
    TenHK = db.Column(db.String(100), nullable=False)
    NamHoc = db.Column(db.Integer, nullable=False)
    diems = db.relationship('Diem', backref='hoc_ky', lazy=True)
    bctks = db.relationship('BaoCaoThongKe', backref='hoc_ky', lazy=True)

    def __init__(self, TenHK, NamHoc):
        self.TenHK = TenHK
        self.NamHoc= NamHoc

class MonHoc(db.Model):
    MaMH = db.Column(db.Integer, primary_key=True)
    TenMH = db.Column(db.String(100), nullable=False)
    diems = db.relationship('Diem', backref='mon_hoc', lazy=True)
    bctks = db.relationship('BaoCaoThongKe', backref='mon_hoc', lazy=True)

def __init__(self, TenMH):
    self.TenMH = TenMH

with app.app_context():
    db.create_all()
class Diem(db.Model):
    MaDiem = db.Column(db.Integer, primary_key=True)
    HocSinh_id = db.Column(db.Integer, db.ForeignKey('hoc_sinh.MaHS'))
    Lop_id = db.Column(db.Integer, db.ForeignKey('lop.MaLop'))
    MonHoc_id = db.Column(db.Integer, db.ForeignKey('mon_hoc.MaMH'))
    HocKy_id = db.Column(db.Integer, db.ForeignKey('hoc_ky.MaHK'))
    diem15ps = db.relationship('Diem15P', backref='diem', lazy=True)
    diem1t = db.relationship('Diem1T', backref='diem', lazy=True, uselist=False)
    diemthi = db.relationship('DiemThi', backref='diem', lazy=True, uselist=False)

    def __init__(self, HocSinh_id, Lop_id, MonHoc_id, HocKy_id):
        self.HocSinh_id=HocSinh_id
        self.Lop_id = Lop_id
        self.MonHoc_id = MonHoc_id
        self.HocKy_id = HocKy_id

with app.app_context():
    db.create_all()

    diem1 = Diem(HocSinh_id=2, Lop_id=1, MonHoc_id=1, HocKy_id=1)
    diem2 = Diem(HocSinh_id=4, Lop_id=2, MonHoc_id=2, HocKy_id=1)
    diem3 = Diem(HocSinh_id=9, Lop_id=3, MonHoc_id=2, HocKy_id=2)
    diem4 = Diem(HocSinh_id=14, Lop_id=3, MonHoc_id=3, HocKy_id=2)
    diem5 = Diem(HocSinh_id=7, Lop_id=2, MonHoc_id=1, HocKy_id=1)

    diem15p1= Diem15P(DiemL1=6, DiemL2=7, Diem_id=16)
    diem15p2 = Diem15P(DiemL1=10, DiemL2=6, Diem_id=17)
    diem15p3 = Diem15P(DiemL1=8, DiemL2=7, Diem_id=18)
    diem15p4 = Diem15P(DiemL1=9, DiemL2=10, Diem_id=19)
    diem15p5 = Diem15P(DiemL1=5, DiemL2=8, Diem_id=20)

    diem1t1= Diem1T(Diem1T=7.3, Diem_id=16)
    diem1t2 = Diem1T(Diem1T=8.6, Diem_id=17)
    diem1t3 = Diem1T(Diem1T=9.8, Diem_id=18)
    diem1t4 = Diem1T(Diem1T=6, Diem_id=19)
    diem1t5 = Diem1T(Diem1T=10, Diem_id=20)

    diemthi1=  DiemThi( DiemThi=6.5, Diem_id=16)
    diemthi2 = DiemThi(DiemThi=7.5, Diem_id=17)
    diemthi3 = DiemThi(DiemThi=10, Diem_id=18)
    diemthi4 = DiemThi(DiemThi=7, Diem_id=19)
    diemthi5 = DiemThi(DiemThi=8.3, Diem_id=20)

with app.app_context():
    db.create_all()
    #db.session.add_all([diem1, diem2, diem3, diem4, diem5])
    #db.session.add_all([diem15p1, diem15p2, diem15p3, diem15p4, diem15p5])
    #db.session.add_all([diem1t1, diem1t2, diem1t3, diem1t4, diem1t5])
    #db.session.add_all([diemthi1, diemthi2, diemthi3, diemthi4, diemthi5])
    db.session.commit()


hs1 = HocSinh(HoTen='Nguyễn Văn An', NgaySinh='23-3-2003', GioiTinh='Nam', DiaChi='13 Đặng Thùy Trâm', SDT='039784124', Email='Anh11@gmail.com', Lop_id=1)
hs2 = HocSinh(HoTen='Trần Ngọc Bảo', NgaySinh='9-4-2003', GioiTinh='Nam', DiaChi='211 Nguyễn Xí', SDT='039091156', Email='Bao93@gmail.com', Lop_id=1)
hs3 = HocSinh(HoTen='Trần Thị Lan', NgaySinh='5-6-2003', GioiTinh='Nữ', DiaChi=' 30 Tân Thới Nhất',SDT='034667790', Email='Lan794@gmail.com', Lop_id=1)
hs4 = HocSinh(HoTen='Tống Ngọc Nhi', NgaySinh='27-11-2003', GioiTinh='Nữ', DiaChi='197/5 Bạch Đằng',SDT='035660023', Email='nhi33@gmail.com', Lop_id=1)
hs5 = HocSinh(HoTen='Lý Thị Sương', NgaySinh='15-3-2002', GioiTinh='Nữ', DiaChi='9 Hoàng Minh Giám',SDT='039446112', Email='suonggg81@gmail.com', Lop_id=2)
hs6 = HocSinh(HoTen='Đỗ Trọng Minh', NgaySinh='18-3-2002', GioiTinh='Nam', DiaChi='136 Nguyễn Hữu Thọ',SDT='035165234', Email='minh_h23@gmail.com', Lop_id=2)
hs7 = HocSinh(HoTen='Lê Thành ', NgaySinh='29-12-2002', GioiTinh='Nam', DiaChi='Cư xá Đồng Tiến',SDT='034776654',Email='Thhanh07@gmail.com', Lop_id=2)
hs8 = HocSinh(HoTen='Huỳnh Văn Phúc', NgaySinh='14-2-2002', GioiTinh='Nam', DiaChi='22 Tôn Đức Thắng', SDT='039005471',Email='Phuc110@gmail.com', Lop_id=2)
hs9 = HocSinh(HoTen='Lê Quỳnh Như ', NgaySinh='7-6-2001', GioiTinh='Nữ', DiaChi=' 94 Khánh Hội', SDT='03567812', Email='Nhu94@gmail.com', Lop_id=3)
hs10 = HocSinh(HoTen='Trương Gia Hân ', NgaySinh='10-3-2001', GioiTinh='Nữ', DiaChi='95 Võ Văn Tần',SDT='035223906',Email='Han1003@gmail.com', Lop_id=3)
hs11 = HocSinh(HoTen='Trần Như Ý ', NgaySinh='23-2-2001', GioiTinh='Nữ', DiaChi=' Cư xá Vĩnh Hội',SDT='034876654',Email='Y232@gmail.com', Lop_id=3)
hs12 = HocSinh(HoTen='Lê Thành Công ', NgaySinh='9-1-2001', GioiTinh='Nam', DiaChi='216 Chu Văn An',SDT='039001369',Email='Cong9121@gmail.com', Lop_id=3)
hs13 = HocSinh(HoTen='Trần Tú', NgaySinh='18-8-2001', GioiTinh='Nam', DiaChi='11 Nguyễn Kiệm', SDT='034772231',Email='Tu183@gmail.com', Lop_id=4)
hs14 = HocSinh(HoTen='Nguyễn Thị Hoa ', NgaySinh='29-12-2001', GioiTinh='Nữ', DiaChi='64 Phổ Quang',SDT='039110654', Email='Hooa491@gmail.com', Lop_id=4)
hs15 = HocSinh(HoTen='Quách Phú Thành', NgaySinh='27-4-2001', GioiTinh='Nam', DiaChi='Cư xá Đồng Tiến',SDT='034436654',Email='thanh27@gmail.com', Lop_id=4)
hs16 = HocSinh(HoTen='Lê Hoàng Trí ', NgaySinh='2-1-2001', GioiTinh='Nam', DiaChi='20 Nguyễn Hữu Cảnh',SDT='03474321', Email='Tri16@gmail.com', Lop_id=4)

lop10_1 = Lop(TenLop='10A1', SiSo=4)
lop11_1= Lop(TenLop='11A1', SiSo=4)
lop12_1= Lop(TenLop='12A1', SiSo=4)
lop12_2= Lop( TenLop='12A2', SiSo=4)

lop10_1.hocsinhs.extend([hs1, hs2, hs3, hs4])
lop11_1.hocsinhs.extend([hs5, hs6, hs7, hs8])
lop12_1.hocsinhs.extend([hs9, hs10, hs11, hs12])
lop12_2.hocsinhs.extend([hs13, hs14, hs15, hs16])

hk1 = HocKy(TenHK='Học kỳ 1', NamHoc=2023)
hk2 = HocKy(TenHK='Học kỳ 2', NamHoc=2024)

mh1 = MonHoc(TenMH='Toán')
mh2 = MonHoc(TenMH='Văn')
mh3 = MonHoc(TenMH='Tiếng anh')

#with app.app_context():
   # db.create_all()
   # db.session.add_all([hs1, hs2, hs3, hs4, hs5, hs6, hs7, hs8, hs9, hs10, hs11, hs12, hs13, hs14, hs15, hs16])
    #db.session.add_all([hk1, hk2])
   #db.session.add_all([mh1, mh2, mh3])
   # db.session.commit()

with app.app_context():
    db.create_all()




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))

def __init__(self, email, password):
    self.email = email
    self.password = password

#with app.app_context():
#    db.create_all()

    user1 = User(email='u111@gmail.com', password='111')
    user2 = User(email='u222@gmail.com', password='222')

   # db.session.add_all([user1, user2])
   # db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)


