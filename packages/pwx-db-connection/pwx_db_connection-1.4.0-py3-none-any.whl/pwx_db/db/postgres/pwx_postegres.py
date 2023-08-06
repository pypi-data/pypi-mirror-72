import psycopg2
from os import getenv


class PostgresDB:
    __slots__ = ['__connection', '__cursor']

    __db_name = getenv('DB_NAME')
    __db_user = getenv('DB_USER')
    __db_password = getenv('DB_PASS')
    __db_host = getenv('DB_HOST')

    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def __connect(self):
        try:
            self.__connection = psycopg2.connect(dbname=self.__db_name,
                                                 user=self.__db_user,
                                                 password=self.__db_password,
                                                 host=self.__db_host)

            self.__cursor = self.__connection.cursor()

        except Exception as ex:
            print(ex)

    def __set_cursor(self):
        self.__cursor = self.__connection.cursor()

    def close_cursor(self):
        if self.__cursor and not self.__cursor.closed:
            self.__cursor.close()

    @property
    def cursor(self):
        self.__check_connection()
        if self.__cursor.closed:
            self.__set_cursor()

        return self.__cursor

    def select_columns(self, table_name):
        try:
            self.__check_connection()

            self.cursor.execute(self.__get_native_sql(table_name))
            result = self.cursor.fetchall()

            if result:
                return result

            raise NameError(f'Table with name [{table_name if table_name else "empty name"}] not exists!')

        except Exception as ex:
            raise ex

        finally:
            self.close_cursor()
            self.__close_connection()

    def execute_query_all(self, sql):
        try:
            self.__check_connection()

            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            if result:
                return result

            return None

        except Exception as ex:
            print(ex, flush=True)
            return None

        finally:
            self.__close_connection()

    def execute_query_one(self, sql):
        try:
            self.__check_connection()

            self.cursor.execute(sql)
            result = self.cursor.fetchone()

            if result:
                return result

            return None

        except Exception as ex:
            print(ex, flush=True)
            return None

        finally:
            self.__close_connection()

    def execute_query(self, sql):
        self.__check_connection()

        try:
            self.cursor.execute(sql)
            self.__connection.commit()

        except Exception as ex:
            print(f'[ERRO SQL] ::: {ex}')
            self.__connection.rollback()

        self.__close_connection()

    def __check_connection(self):
        if not self.__connection or self.__connection.closed:
            self.__connect()

    def __close_connection(self):
        if not self.__connection.closed:
            self.__connection.close()
            self.close_cursor()

    @staticmethod
    def __get_native_sql(table_name):
        return f"SELECT column_name FROM information_schema.columns where table_name = '{table_name}'"
