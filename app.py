from flask import Flask, render_template, request, redirect, url_for
from forms import LoginForm, RegisterForm

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
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(phone, password)
        return redirect('basic')
    return render_template('login.html', form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def Register():
    register_form = RegisterForm()
    return render_template('register.html', form=register_form)

@app.route('/basic')
def Basic():
    return render_template('basic.html')

@app.route('/fansfluct')
def FansFluct():
    return render_template('fansfluct.html')

@app.route('/activedata')
def ActiveData():
    return render_template('activedata.html')

@app.route('/category')
def Category():
    return render_template('category.html')


if __name__ == '__main__':
    app.run()
