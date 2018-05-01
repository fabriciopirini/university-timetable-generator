import os
from flask import Flask, request, render_template
from scrap import SIGAA
import time
from initial_config import *
from models import *


class FlaskService(object):

    def __init__(self):
        pass

    def do_function(self):
        @APP.route('/', methods=["POST"])
        def pesquisa_disciplina():
            texto = "".join(['%', request.form.get('pesquisa').upper(), '%'])
            try:
                qtde = Disciplina.query.filter(
                    Disciplina.nome.like(texto)).count()
                if qtde > 0:
                    resultado = Disciplina.query.filter(
                        Disciplina.nome.like(texto)).all()
                    #resultado = Disciplina.query.filter_by(nome='ECOI14.1 - Banco de Dados').all()
                    resultado = (str(disciplina.nome)
                                 for disciplina in resultado)
                    # return (str(disciplina.nome) for disciplina in resultado)
                    return render_template('index.html', disciplinas=resultado)
                else:
                    return render_template('index.html', disciplinas='')
            except:
                print("Pesquisa não rolou")
                return("Algo de errado não está certo!")

        @APP.route('/', methods=["GET"])
        def inicio():
            return render_template('index.html', disciplinas='')

        @APP.route('/disciplinas')
        def visualiza_disciplinas_registradas():
            disciplinas = Disciplina.query.all()
            return render_template('lista_disciplinas.html', disciplinas=disciplinas)

        @APP.route('/registra_disciplinas', methods=['GET'])
        def formulario_registra_disciplinas():
            return render_template('registra_disciplinas.html')

        @APP.route('/registra_disciplinas', methods=['POST'])
        def registra_disciplinas():
            # siglaCurso = request.form.get('siglaCurso')
            cursos = ['EAM', 'EMO', 'ECO', 'ECA',
                      'EMT', 'EPR', 'ESS', 'EEL', 'EME']
            ano = request.form.get('ano')
            semestre = request.form.get('semestre')
            for siglaCurso in cursos:
                x, y = SIGAA.retorna_turmas(siglaCurso, ano, semestre)
                d = SIGAA.format(x, y)
                # DB.session.query('disciplinas').delete()
                # DB.session.commit()
                for item in d:
                    disciplina = Disciplina(
                        item.upper(), 'Campus Itabira', siglaCurso)
                    DB.session.add(disciplina)
                    DB.session.commit()
                print(' '.join(['Curso processado:', siglaCurso]))
                time.sleep(1)
            # for item in d:
            #     turma = Turma(item, 'Campus Itabira')
            #     DB.session.add(disciplina)
            #     DB.session.commit()
            # name = request.form.get('name')
            # email = request.form.get('email')

            # guest = Guest(name, email)
            # DB.session.add(guest)
            # DB.session.commit()

            # return render_template('guest_confirmation.html', name=name, email=email)
            return render_template('confirma_registro.html')

            if __name__ == '__main__':
                app.run(debug=True)


p = FlaskService()
p.do_function()
