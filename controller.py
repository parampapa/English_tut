"""
Модуль включает в себя ряд маршрутов  и обработчиков для управления.

Функции:
- index(): Главная страница приложения.
- login(): Обработка входа в систему.
- register(): Обработка регистрации новых пользователей.
- secret(): Доступ к секретной странице.
- logout(): Выполняет выход пользователя из системы.
- redirect_to_sign(): Перенаправляет неавторизованных пользователей на
страницу входа.
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from models import User


@app.route('/', methods=['GET'])
def index():
    """
    Обрабатывает главную страницу приложения, отображая базовый шаблон.

    Returns:
        str: HTML-шаблон 'base.html' для отображения главной страницы.
    """
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Обрабатывает страницу входа. При GET запросе отображает страницу
    авторизации.
    При POST запросе выполняет проверку учетных данных пользователя и, в
    случае успеха, перенаправляет на главную страницу, иначе выводит
    сообщение об ошибке.

    Returns:
        werkzeug.wrappers.Response: Объект Response с перенаправлением:
            - на главную страницу при успешном входе
            - обратно на страницу входа при ошибке авторизации.
    """
    if current_user.is_authenticated:
        # Если пользователь уже залогинен, перенаправляем его на главную страницу
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login.html')
    login = request.form.get('login')
    password = request.form.get('password')
    user = User.query.filter_by(login=login).first()
    if user is None or not check_password_hash(user.password, password):
        flash('Неверный логин или пароль.')
        return redirect(url_for('login'))
    login_user(user)
    flash({'title': "Статус", 'message': "Успешная авторизация"},
          'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Обрабатывает страницу регистрации. При GET запросе отображает страницу
    регистрации.
    При POST запросе создает нового пользователя и, если регистрация прошла
    успешно, выполняет вход и перенаправляет на главную страницу.

    Returns:
        werkzeug.wrappers.Response: Объект Response с перенаправлением:
            - на главную страницу при успешной регистрации
            - обратно на страницу регистрации при возникновении ошибки.
     """
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
def secret():
    """
    Отображает пока секретный текст. Доступ к странице имеют только
    аутентифицированные пользователи.

    Returns:
        str: Строка с информационным сообщением о продуктах, предназначенная
        для зарегистрированных пользователей.
    """
    return '<h1>Здесь будет инфа для зарегистрированных пользователей</h1>'


@app.route('/logout')
@login_required
def logout():
    """
    Выполняет выход пользователя из системы и перенаправляет на главную
    страницу.

    Returns:
        werkzeug.wrappers.Response: Объект Response с перенаправлением на
        главную страницу.
    """
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_sign(response):
    """
    Перенаправление на страницу аутентификации в случае отсутствия
    авторизации

    Эта функция вызывается автоматически после каждого запроса. Она проверяет
    статусный код ответа. Если статусный код ответа равен 401 (Неавторизован),
    происходит перенаправление пользователя на страницу регистрации и
    авторизации. Это обеспечивает, что пользователи, пытающиеся получить доступ
    к защищенным ресурсам без соответствующих прав доступа, будут направлены к
    форме входа, вместо отображения стандартной страницы с ошибкой 401.

    Args:
        response: werkzeug.wrappers.Response - Объект ответа, сгенерированный
        обработчиками запросов.

    Returns:
        werkzeug.wrappers.Response: Исходный объект ответа или объект
        перенаправления на страницу входа при статусе 401.
    """
    if response.status_code == 401:
        return redirect(url_for('login'))
    return response
