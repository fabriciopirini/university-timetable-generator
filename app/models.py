from initial_config import *


class Disciplina(DB.Model):
    """Modelo de banco de dados para monitorar as disciplinas."""

    __tablename__ = 'disciplinas'
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.String(150))
    campus = DB.Column(DB.String(30))
    curso = DB.Column(DB.String(5))

    def __init__(self, nome=None, campus=None, curso=None):
        self.nome = nome
        self.campus = campus
        self.curso = curso


class Turma(DB.Model):
    """Modelo de banco de dados para monitorar cada turma e linkar com as disciplinas."""

    __tablename__ = 'turmas'
    id = DB.Column(DB.Integer, primary_key=True)
    idDisciplina = DB.Column(DB.Integer, DB.ForeignKey(
        'disciplinas.id'), primary_key=True)
    periodo = DB.Column(DB.String(10))
    nivel = DB.Column(DB.String(10))
    turma = DB.Column(DB.String(10))
    docente = DB.Column(DB.String(100))
    situacao = DB.Column(DB.String(10))
    horario = DB.Column(DB.String(1000))
    local = DB.Column(DB.String(30))
    matriculados = DB.Column(DB.String(30))

    def __init__(self, idDisciplina, periodo=None, nivel=None, turma=None, docente=None, situacao=None, horario=None, local=None, matriculados=None):
        self.idDisciplina = idDisciplina
        self.periodo = periodo
        self.nivel = nivel
        self.turma = turma
        self.docente = docente
        self.situacao = situacao
        self.horario = horario
        self.local = local
        self.matriculados = matriculados
