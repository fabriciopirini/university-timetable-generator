from models import db
from flask import Flask, render_template, jsonify, make_response, redirect, request, url_for
#import GenericDBConnection
from scrap import SIGAA

app = Flask(__name__)

POSTGRES = {
    'user': 'aluno',
    'pw': 'abc123-',
    'db': 'disciplinas',
    'host': '127.0.0.1',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

db.init_app(app)

def __init__(self):
    pass

def do_function(self):
    app = Flask(__name__)

    @app.route('/index')
    @app.route('/')
    def index():
        return render_template('index.html', data=SIGAA.retorna_turmas())

    if __name__ == '__main__':
        app.run()

#p = FlaskService()
#p.do_function()