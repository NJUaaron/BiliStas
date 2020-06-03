from flask import Flask, render_template, request, redirect, url_for
from forms import LoginForm, RegisterForm
import sqlite3
import dbutils

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if request.method == 'POST':
        phone = request.form.get('phone', type=str)
        password = request.form.get('password', type=str)
        conn = sqlite3.connect("bilistat.db")
        c = conn.cursor()
        result = c.execute("SELECT PASSWORD FROM ACCOUNTS WHERE USERNAME='"+str(phone)+"';")
        pasw = ""
        for row in result:
            pasw = row[0]
        if pasw == password:
            return redirect('basic')
    return render_template('login.html', form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def Register():
    register_form = RegisterForm()
    if request.method == 'POST':
        phone = request.form.get('phone', type=str)
        password = request.form.get('password', type=str)
        conn = sqlite3.connect("bilistat.db")
        c = conn.cursor()
        result = c.execute("SELECT PASSWORD FROM ACCOUNTS WHERE USERNAME='"+str(phone)+"';")
        conn.commit()
        pasw = ""
        for row in result:
            pasw = row[0]
        if pasw != "":
            return redirect('register.html')
        else:
            c.execute("INSERT INTO ACCOUNTS (USERNAME, PASSWORD) VALUES (?,?);", (phone, password))
            conn.commit()
            return redirect('login')
    return render_template('register.html', form=register_form)


@app.route('/basic')
def Basic():
    conn = sqlite3.connect("bilistat.db")
    r = dbutils.gettop2up(conn)
    top10 = dbutils.gettop10up(conn)
    dayrank = dbutils.getdayrank10(conn)
    monthrank = dbutils.getmonthrank10(conn)
    conn.close()
    return render_template('basic.html', top1_up=r[0][0], top1_funs=r[0][1],
                           top2_up=r[1][0], top2_funs=r[1][1], top1_face=r[0][2], top2_face=r[1][2], top10=top10,
                           dayrank=dayrank, monthrank=monthrank)


@app.route('/activedata')
def ActiveData():
    return render_template('activedata.html')


@app.route('/category')
def Category():
    return render_template('category.html')


if __name__ == '__main__':
    app.run()
