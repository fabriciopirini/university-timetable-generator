from flask import Flask, request, render_template
from scrap import SIGAA
import time
from initial_config import *
from models import *
import numpy as np
import logging


class FlaskService(object):

    def __init__(self):
        pass

    def do_function(self):
        @APP.route('/', methods=["POST"])
        def pesquisa_disciplina():
            if(request.form.get('pesquisa') == ""):
                return render_template('index.html', disciplinas='', turmas='')
            texto = "".join(['%', request.form.get('pesquisa').upper(), '%'])
            resultadoTurmas = []
            resultadoDisciplinas = []
            try:
                logging.info("Inicio try")
                qtde = Disciplina.query.filter(Disciplina.nome.like(texto)).count()
                logging.info(str(qtde))
                if qtde > 0:
                    resultado = Disciplina.query.filter(Disciplina.nome.like(texto)).order_by(Disciplina.nome.asc()).all()

                    for item in resultado:
                        resultadoDisciplinas.append([item.id, item.nome, item.curso])
                        # print("Dados disciplinas")
                        listaTurmas = Turma.query.filter_by(idDisciplina=item.id).order_by(Turma.curso.asc(), Turma.turma.asc()).all()
                        # print("Turmas pesquisadas")
                        for item2 in listaTurmas:
                            # print(' '.join([item]))
                            resultadoTurmas.append([item2.idDisciplina, item2.turma, item2.docente, item2.horario])
                            # print("Lista de turmas criadas")
                    # print(resultadoTurmas)
                    # resultadoTurmas = Turma.query.filter_by(idDisciplina=resultado.id).all()
                    # resultado = Disciplina.query.filter_by(nome='ECOI14.1 - Banco de Dados').all()
                    # resultado = (str(disciplina.nome) for disciplina in resultado)
                    # return (str(disciplina.nome) for disciplina in resultado)
                    return render_template('index.html', disciplinas=resultadoDisciplinas, turmas=resultadoTurmas)
                else:
                    return render_template('index.html', disciplinas='0', turmas='')
            except:
                logging.warning("Pesquisa não rolou")
                return render_template('index.html', disciplinas='1', turmas='')

        @APP.route('/', methods=["GET"])
        def inicio():
            return render_template('index.html', disciplinas='', turmas='')

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
                for item, info in d.items():
                    disciplina = Disciplina(
                        item.upper(), 'Campus Itabira', siglaCurso)
                    DB.session.add(disciplina)
                    DB.session.commit()
                    DB.session.refresh(disciplina)
                    for i in np.arange(0, len(info), 8):
                        turma = Turma(disciplina.id, info[i], info[i + 1], info[i + 2], info[i + 3], info[i + 4],
                                      info[i + 5], info[i + 6], info[i + 7], siglaCurso)
                        DB.session.add(turma)
                        # DB.session.commit()
                        # print(': '.join([str(i % 8), str(elemento)]))
                print(' '.join(['Curso processado:', siglaCurso]))
                DB.session.commit()
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
