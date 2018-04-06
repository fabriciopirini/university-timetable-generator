import configparser
import os
import psycopg2
from flask import Flask, render_template, jsonify, make_response, redirect, request, url_for
import GenericDBConnection
from scrap import SIGAA

class FlaskService(object):

    app = Flask(__name__)

    def __init__(self):
        pass

    def do_function(self):
        app = Flask(__name__)

        @app.route('/index')
        @app.route('/')
        def index():
            return render_template('index.html', data=SIGAA.retorna_turmas())

        if __name__ == '__main__':
            app.run(debug=True)
p = FlaskService()
p.do_function()
