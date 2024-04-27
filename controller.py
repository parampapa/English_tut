from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()
    if user and not check_password_hash(user.password, password):
        flash('Неверный логин или пароль.')
        return redirect(url_for('login'))
    login_user(user)
    flash({'title': "Статус", 'message': "Успешная авторизация"},
          'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    login = request.form.get('login')
    password = request.form.get('password')
    if not (3 < len(login) < 32 and 3 < len(password) < 32):
        flash('Логин и пароль должны быть от 4 до 31 символов.')
        return redirect(url_for('register'))
    password = generate_password_hash(password)
    user = User(login=login, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    except IntegrityError:
        flash('Данный логин уже используется.')
        return redirect(url_for('register'))
    # Пользователь с таким логином уже зарегистрирован



@app.route('/products')
@login_required
def products():
    return '<h1>Здесь будет инфа для зарегистрированных пользователей</h1>'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response
