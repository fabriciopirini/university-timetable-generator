""" This file is responsible to provide database connection """
from collections import OrderedDict
import configparser
import psycopg2

class Database(object):
    """ Class responsible for create a Postgres connection """

    __instance = None
    __host = None
    __user = None
    __password = None
    __database = None
    __port = None
    __session = None
    __connection = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or not cls.__database:
            cls.__instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.__instance
    ## End def __new__

    def __init__(self):

        config = ConfigParser.RawConfigParser()
        config.read('config_file.properties')
        database = config.get('DatabaseSection', 'db.database')
        user = config.get('DatabaseSection', 'db.user')
        password = config.get('DatabaseSection', 'db.password')
        host = config.get('DatabaseSection', 'db.host')
        port = config.get('DatabaseSection', 'db.port')

        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
    ## End def __init__

    def __open(self):
        try:
            cnx = psycopg2.connect(host=self.__host,
                                   user=self.__user,
                                   password=self.__password,
                                   dbname=self.__database,
                                   port=self.__port)
            self.__connection = cnx
            self.__session = cnx.cursor()
        except psycopg2.Error as err:
            print ("Error %d: %s" % (err.args[0], err.args[1]))
    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    ## End def __close

    def insert(self, table, *args, **kwargs):
        """
        generic insert method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection

        CONN = repository.GenericDBConnection.Database()
        CONN.insert("tb_atom_interface", atom_1="8231", atom_2="8784", area="2.655",
            algorithm="TEST", distance='0')

        """
        # Esse codigo foi alterado para que retornasse o ID inserido a quem chamou a funcao

        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["%s"] * len(keys)) % tuple(keys) + ")"
            # Usando o RETURNING * no fim do INSERT retorna tudo o que foi inserido, inclusindo o ID
            query += " VALUES ("+",".join(["%s"]*len(values)) + ") RETURNING *"
            # query += " VALUES ("+",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            # Usando o RETURNING * no fim do INSERT retorna tudo o que foi inserido, inclusindo o ID
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ") RETURNING *"
            # query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        # Linha inserida para pegar o primeiro registro dos inseridos e o primeiro campo (ID)
        try:
            retorno = self.__session.fetchall()[0][0]
        except ValueError:
            print (self.__session.fetchall())
        self.__connection.commit()
        self.__close()
        # Como nao estava funcionando o lastrowid (parece que e so no MySQL), mudei
        # return self.__session.lastrowid
        return retorno
    ## End def insert

    def delete(self, table, where=None, *args):
        """
        generic delete method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection

        CONDITIONAL_QUERY = 'algorithm = %s'

        RESULT = CONN.delete("tb_atom_interface", CONDITIONAL_QUERY, "TEST")
        print RESULT

        the result value will be the exact number of rows deleted

        """
        query = "DELETE FROM %s" % table
        if where:
            query += ' WHERE %s' % where

        values = tuple(args)

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        delete_rows = self.__session.rowcount
        self.__close()

        return delete_rows
    ## End def delete

    def update(self, table, where=None, *args, **kwargs):
        """
        generic update method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection

        CONDITIONAL_QUERY = 'algorithm = %s'

        RESULT = CONN.update("tb_atom_interface", CONDITIONAL_QUERY, "TEST", distance='99')
        print RESULT

        the result value will be the exact number of rows updated

        """
        query = "UPDATE %s SET " % table
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        args_len = len(keys) - 1
        for i, key in enumerate(keys):
            query += key+" = %s"
            if i < args_len:
                query += ","
            ## End if i less than 1
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows

    def select(self, table, where=None, *args, **kwargs):
        """
        generic simple select method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection

        CONDITIONAL_QUERY = 'algorithm = %s'

        RESULT = CONN.select("tb_atom_interface", CONDITIONAL_QUERY, "*", algorithm="TEST")

        RESULT_2 = CONN.select("tb_atom_interface", CONDITIONAL_QUERY,
                               "atom_1", "atom_2", algorithm="TEST")

        the result value will be the fech

        """
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        args_len = len(keys) - 1

        for i, key in enumerate(keys):
            query += key+""
            if i < args_len:
                query += ","
        ## End for keys

        query += ' FROM %s' % table

        if where:
            query += " WHERE %s" % where
        ## End if where

        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()

        return result
    ## End def select

    def select_advanced(self, sql, *args):
        """
        generic advanced select method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection

        SQL_QUERY = "SELECT * FROM tb_atom_interface ai"
        SQL_QUERY += " WHERE ai.algorithm = %s AND ai.distance < %s"

        RESULT = CONN.select_advanced(SQL_QUERY, ("algorithm", "TEST"), ("distance", " 100"))

        the result value will be the fech

        """
        order_direct = OrderedDict(args)
        query = sql
        values = tuple(order_direct.values())
        self.__open()
        self.__session.execute(query, values)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]

        self.__close()
        return result
    ## End def select_advanced

    def call_store_procedure(self, name, *args):
        """
        generic call procedure and function method

        In order to use this method, you just need to call like this:
        import repository.GenericDBConnection
        CONN = repository.GenericDBConnection.Database()
        RESULT = CONN.call_store_procedure(procedure_name, values)

        the result value will be returned by fetchall

        """
        result_sp = None
        self.__open()
        self.__session.callproc(name, args)
        self.__connection.commit()
        # for result in self.__session.stored_results():
        #     result_sp = result.fetchall()
        self.__close()
        return result_sp
    ## End def call_store_procedure

## End class Connection()
