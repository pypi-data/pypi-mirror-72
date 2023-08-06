from re import sub
from pwx_db import PostgresDB, Native
from datetime import datetime


class PersistSync:

    __slots__ = ['__table_name', '__columns', '__values', '__sql_delete', '__sql_insert', '__ids', '__update',
                 '__where_columns', '__where_values', '__only_insert', '__many']

    __db = PostgresDB()

    def __init__(self, table_name):
        self.__table_name = table_name
        self.__ids = []

    def __init(self, columns, values, many, only_insert, update, where_columns, where_values):
        self.__update = update
        self.__only_insert = only_insert if not self.__update else True
        self.__many = many if not self.__update else False
        self.__columns = columns
        self.__values = values
        self.__where_columns = where_columns
        self.__where_values = where_values

        if not only_insert:
            self.__get_ids()

    def persist(self, columns, values, many=False, only_insert=False, update=False, where_columns=None,
                where_values=None):
        self.__init(columns, values, many, only_insert, update, where_columns, where_values)
        self.__prepare_sql()
        self.__execute()
        self.__ids = []

    def __get_ids(self):
        if isinstance(self.__values[0], list):
            for value in self.__values:
                self.__ids.append(int(value[0]))  # first position always be id
        else:
            self.__ids.append(self.__values[0])

    def __prepare_sql(self):
        if not self.__only_insert:
            self.__sql_delete = Native.delete_by_id(table_name=self.__table_name, ident=self.__get_string(self.__ids))

        if not self.__update:
            self.__sql_insert = Native.insert(table_name=self.__table_name,
                                              colunms=self.__get_string(self.__columns, is_columns=True),
                                              values=self.__get_string(self.__values, self.__many))

        self.__sql_insert = Native.update(table_name=self.__table_name,
                                          sets=self.__string_update(where=False),
                                          where=self.__string_update(where=True))

    def __get_string(self, values_to_str, many=False, is_columns=False):
        if many:
            return self.__many_values(values_to_str, is_columns)

        return self.__to_string(values_to_str, is_columns)

    def __to_string(self, values_to_str, is_columns):
        return f"({', '.join([self.__convert(value, is_columns) for value in values_to_str])})"

    @staticmethod
    def __convert(value, is_columns):
        if is_columns:
            return str(value)

        elif isinstance(value, bool):
            return f"'{str(value).lower()}'"

        elif isinstance(value, int) or isinstance(value, float):
            return str(value)

        elif isinstance(value, str):
            return f"'{value.lower()}'"

        elif isinstance(value, datetime):
            return f"'{str(value)}'"

        elif not value:
            return 'null'

    def __many_values(self, values_to_str, is_columns):
        val = ''
        for value in values_to_str:
            val += f'{self.__to_string(value, is_columns)},'

        return sub('[,]$', ';', val)

    def __execute(self):
        if not self.__only_insert:
            self.__execute_delete()

        self.__execute_insert()

    def __execute_delete(self):
        self.__db.execute_query(sql=self.__sql_delete)

    def __execute_insert(self):
        self.__db.execute_query(sql=self.__sql_insert)

    def __string_update(self, where=False):
        cols = self.__columns if not where else self.__where_columns
        vals = self.__values if not where else self.__where_values

        query = ''
        for position in range(len(cols)):
            column = self.__convert(cols[position], is_columns=True)
            value = self.__convert(vals[position], is_columns=False)

            if not where:
                query += f'{column} = {value}, '
            else:
                query += f'{column} = {value} AND '

        if not where:
            return sub('(,\\s+)$', '', query)

        return sub('(\\s+AND\\s+)$', ';', query)
