from app import app,db
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import *
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')

@login_required
def index():
    user = {'username':'duke'}
    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块循环中的例子2'
                   ''
        },
        {
            'author': {'username': '哈哈'},
            'body': '这是模板模块循环中的例子1'
        }
    ]
    return render_template('index.html',user=user,title='我的',posts=posts)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("无效的用户名或密码")
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('index'))
        # flash("用户登录用户名是{},是否记住我{}".format(form.username.data,form.remember_me.data))
        # return redirect(url_for("index"))
    return render_template("login.html",title="登录",form=form,book="大道朝天")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/regiser',methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data,email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for('login'))
    return render_template("register.html", title="注册", form=form)

@app.route('/book/<books>',methods=["GET","POST"])
def book(books):
    id = Books.query.filter_by(bookname=books).first().id
    print(id)
    value = Booksection.query.filter_by(book_id=id).all()
    return render_template("test.html",value=value)

@app.route('/section/<id>',methods=["GET","POST"])
def section(id):
    book = Booksection.query.filter_by(section_id=id).first().section_path
    print(book)
    f = open("%s"%book)
    value = [i for i in f.readlines()]
    return render_template("read.html",value=value)


