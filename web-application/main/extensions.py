# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CsrfProtect
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf_protect = CsrfProtect()
login_manager = LoginManager()
