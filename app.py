import uuid

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['TOASTR_TIMEOUT'] = 3000
db = SQLAlchemy(app)
manager = LoginManager(app)
toastr = Toastr(app)