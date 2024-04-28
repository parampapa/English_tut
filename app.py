import uuid

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr


# Инициализация основного объекта Flask
app = Flask(__name__)

# Настройка параметров приложения Flask

# URI для подключения к базе данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Генерация уникального секретного ключа для сессии
app.config['SECRET_KEY'] = str(uuid.uuid4())

# Установка времени показа Toastr уведомлений (в миллисекундах)
app.config['TOASTR_TIMEOUT'] = 3000

# Инициализация объекта SQLAlchemy для взаимодействия с базой данных
db = SQLAlchemy(app)

# Инициализация менеджера пользовательских сессий для Flask приложения
manager = LoginManager(app)

# Инициализация объекта Toastr для вывода всплывающих сообщений
toastr = Toastr(app)
