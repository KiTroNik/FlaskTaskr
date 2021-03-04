import os
import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)

#app.config.from_pyfile('_config.py')
app.config['DATABASE'] = 'flasktaskr.db'
app.config['WTF_CSRF_ENABLED'] = True
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = """a7d9a636c6ecf8 d3598171dbde62 7ded3d05c22a5e bcc5fad457d3a5 3ce6fdf59da2de
ad448cfd98b994 9ffe8a4037feb5 1006389f11fe61 f924a9f1aca191 5469d7c70d492d
8471b514f6eefe 36d83380c99b5c cff80eb0788391 56045e744d68bd 84b58d6ebcb2af
d7bc70a5ad2c32 486408d0573c04 c9929bc25f4a4c 1e0591f39764cf b936e2c45f97cc
5c593500fefaab 4c62df00565dea ca29fe4e5c6787 cb098f7a79b14d 4621ae7855e7c3
ca8db020f825d6 e5869c6c9e62f0 2720f5c72b04a4 299965df6b1f8a 1e334b13a97d91
83fcd0426983ab 2fd0472f017e9b 01349f06e83a5f 658a910da171ff e56545c9929197
08fb2ba42bc167 a02ec44812f7f7 bad03fda9121ef 1b35276bc989d9 18acbf91898ac5"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flasktaskr.db')

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)


@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write('\n404 error at {}: {}'.format(current_timestamp, r))
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if app.debug is not True:
        now = datetime.datetime.now()
        r = request.url
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write('\n500 error at {}: {}'.format(current_timestamp, r))
    return render_template('500.html'), 500
    