from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import smtplib
import os

# print(os.environ["MK"])
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sim.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class SimSo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sothuebao = db.Column(db.String(250), nullable=False)
    gia = db.Column(db.String(250), nullable=False)
    dangso = db.Column(db.String(250), nullable=False)
class SimSoTraSau(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sothuebao = db.Column(db.String(250), nullable=False)
    goicuoc = db.Column(db.String(250), nullable=False)
    dangso = db.Column(db.String(250), nullable=False)

class GoiCuoc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tengoi = db.Column(db.String(250), nullable=False)
    gia = db.Column(db.Integer, nullable=False)
    uudaichinh = db.Column(db.String(1000), nullable=False)
    uudaidata = db.Column(db.String(500), nullable=True)
    uudaithoai = db.Column(db.String(1000), nullable=True)
    nhom = db.Column(db.String(250), nullable=True)
    loai = db.Column(db.String(250), nullable=False)

db.create_all()
# for i in range(20):
#     sim = SimSo(sothuebao="0939988383",gia="1.000.000",dangso="ABAB")
#     db.session.add(sim)
#     db.session.commit()
class Sim:
    def __init__(self, id,stb, gia):
        self.id = id
        self.stb = stb
        self.gia = gia
class ShowSimTT(FlaskForm):
    hoten = StringField('Họ tên:', validators=[DataRequired()])
    diachi = StringField('Địa chỉ:', validators=[DataRequired()])
    solienhe = StringField('Số điện thoại:', validators=[DataRequired()])


@app.route('/tratruoc/dathang',methods=["GET","POST"])
def show_tt():
    form = ShowSimTT()
    stb = request.args.get('stb')
    gia = request.args.get('gia')
    print(stb)
    if form.validate_on_submit():
        stb = request.args.get('stb')
        gia = request.args.get('gia')

        my_email = "cuongpython2021@gmail.com"
        password = os.environ.get("MK")
        print(password)
        your_email = "cuongtq88@gmail.com"

        with smtplib.SMTP("smtp.gmail.com") as conection:

            msg = f"Khách hàng {form.hoten.data} \nĐịa chỉ {form.diachi.data} \nSố liên hệ {form.solienhe.data} \nSố mua {stb} \nGiá {gia}"
            subject = "Đơn hàng"
            conection.starttls()
            conection.login(my_email, password)
            # conection.sendmail(from_addr= my_email, to_addrs=your_email,
            #                    msg=f"Subject:Hello \n\n {ten} ")
            fmt = 'From: {}\r\nTo: {}\r\nSubject: {}\r\n{}'
            conection.sendmail(my_email, your_email,fmt.format(my_email,your_email,subject,msg).encode('utf-8'))
        return redirect(url_for('chotdontt'))
    # if request.method == 'POST':
    #     return redirect(url_for('home'))
    return render_template('dathangtt.html', form =form, stb=stb, gia=gia)
@app.route('/')
def home():
    # os.environ["MK"] = "NguyenThiCuc@8383"
    print(os.environ.get("MAT_KHAU"))

    return render_template('index.html')

@app.route('/chotdontt')
def chotdontt():
    return render_template('chotdontt.html')

@app.route('/tracuuso')
def tracuu():
    return redirect(url_for('tratruoc'))

@app.route("/tratruoc", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tratruoc/<int:page>',methods=["GET","POST"])
def tratruoc(page):
    page = page
    print(page)
    pages = 10
    all_sim = SimSo.query.paginate(page,pages,error_out=False)
    if request.method == 'POST' and 'cars' in request.form and 'socantim' in request.form:
        socantim = request.form["socantim"]
        dangso = request.form["cars"]
        if dangso != "All" and socantim !="":
            search = "%{}%".format(socantim)
            all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page, pages, error_out=False)
            print("aaa")
            return render_template('tratruoc.html', all_sim=all_sim, dangso="All", socantim="")
    if request.method == 'POST' and 'cars' in request.form:
        page = 1
        dangso = request.form["cars"]
        socantim = request.form["socantim"]
        dangso_ts = SimSoTraSau.query.filter_by(dangso=dangso).all()
        print("xxx")
        print(dangso_ts)
        if dangso != "All" and socantim == "":
            all_sim = SimSo.query.filter_by(dangso=dangso).paginate(page,pages,error_out=False)

        elif dangso == "All" and socantim == "":
            all_sim = SimSo.query.paginate(page,pages,error_out=False)



        elif socantim != "":
            socantim = request.form["socantim"]
            search = "%{}%".format(socantim)
            all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page,pages,error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, dangso=dangso, socantim = socantim)
    dangso = request.args.get('dangso')
    socantim = request.args.get('socantim')

    if dangso != "" and dangso !=None and dangso != "All":
        all_sim = SimSo.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, dangso=dangso)
    elif socantim != "" and socantim != None:
        search = "%{}%".format(socantim)
        all_sim = SimSo.query.filter(SimSo.sothuebao.like(search)).paginate(page, pages, error_out=False)
        return render_template('tratruoc.html', all_sim=all_sim, socantim=socantim)
    return render_template('tratruoc.html', all_sim = all_sim, dangso="All")


@app.route("/trasau", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tracuusotrasau/<int:page>',methods=["GET","POST"])
def trasau(page):

    page = page
    pages = 10
    all_sim = SimSoTraSau.query.paginate(page,pages,error_out=False)


    if request.method == 'POST' and 'cars' in request.form and 'socantim' in request.form:
        socantim = request.form["socantim"]
        dangso = request.form["cars"]
        print(dangso)
        print(socantim)

        if dangso == "All" and socantim !="":

            search = "%{}%".format(socantim)
            all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page, pages, error_out=False)
            return render_template('trasau.html', all_sim_ts=all_sim, dangso="All", socantim=socantim)
        elif dangso != "All" and socantim != "":

            all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)

            return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso, socantim="")
    if request.method == 'POST' and 'cars' in request.form:

        page = 1
        dangso = request.form["cars"]
        socantim = request.form["socantim"]
        # dangso_ts = SimSoTraSau.query.filter_by(dangso=dangso).all()
        # print("xxx")
        # print(dangso_ts)
        if dangso != "All" and socantim == "":

            all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page,pages,error_out=False)

        elif dangso == "All" and socantim == "":

            all_sim = SimSoTraSau.query.paginate(page,pages,error_out=False)

        elif socantim != "":

            socantim = request.form["socantim"]
            search = "%{}%".format(socantim)
            all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page,pages,error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso, socantim = socantim)
    dangso = request.args.get('dangso')
    socantim = request.args.get('socantim')
    print(dangso)
    if dangso != "" and dangso !=None and dangso != "All":
        all_sim = SimSoTraSau.query.filter_by(dangso=dangso).paginate(page, pages, error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, dangso=dangso)
    elif socantim != "" and socantim != None:
        search = "%{}%".format(socantim)
        all_sim = SimSoTraSau.query.filter(SimSoTraSau.sothuebao.like(search)).paginate(page, pages, error_out=False)
        return render_template('trasau.html', all_sim_ts=all_sim, socantim=socantim)
    return render_template('trasau.html', all_sim_ts = all_sim, dangso="All")

@app.route("/goicuoc", methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/tracuugoi/<int:page>',methods=["GET","POST"])
def goicuoc(page):
    page = page
    pages = 6
    all_goi = GoiCuoc.query.filter_by(nhom="Phổ Biến").paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'loaigoi' in request.form:
        loaigoi = request.form["loaigoi"]
        print(loaigoi)
        all_goi = GoiCuoc.query.filter_by(loai=loaigoi).paginate(page, pages, error_out=False)
        return render_template('goicuoc.html', all_goi=all_goi, loaigoi=loaigoi)
    loaigoi = request.args.get('loaigoi')
    print(loaigoi)
    if loaigoi != "" and loaigoi !=None:
        print("aaa")
        all_goi = GoiCuoc.query.filter_by(loai=loaigoi).paginate(page, pages, error_out=False)
        return render_template('goicuoc.html', all_goi=all_goi, loaigoi=loaigoi)
    return render_template('goicuoc.html', all_goi=all_goi)



if __name__ == "__main__":
    app.run(debug=True)