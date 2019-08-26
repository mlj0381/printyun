from flask import Flask

from app.control.printer import printer
from app.control.login import login
from app.control.admin import admin
from app.control.json import jsons
from app.test.test_route import test
from app.test.ali_pay import cloud_pay
from app.models import db, User
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)



app.config.from_pyfile('config.py')
app.register_blueprint(printer, url_prefix='/printer')
app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(cloud_pay, url_prefix='/cloud_pay')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(jsons, url_prefix='/jsons')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login.back_login'
login_manager.login_message = u'请先登录！'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


from app import print, models, printer,admin