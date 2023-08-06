from json import dumps
from pwx_db import PostgresDB
from datetime import datetime

db = PostgresDB()


class EntitySync:

    __table_name__ = ''

    def __init__(self, name):
        self.__table_name__ = name

    def __sync_attrs__(self):
        try:
            for attr in db.select_columns(self.__table_name__):
                setattr(self, attr[0], None)

        except NameError as ne:
            raise NameError(ne.args[0])

    def __get_attrs__(self):
        return [attr for attr in self.__dict__.keys() if not self.__is_table_name(attr)]

    def __set_values__(self, values):
        attrs = self.__get_attrs__()
        for i in range(len(attrs)):
            self.__setattr__(attrs[i], values[i])

    def __to_json__(self, values=None):
        self.__set_values__(values)

        json = {}

        for attr, value in self.__dict__.items():
            if not self.__is_table_name(attr):

                if isinstance(value, datetime):
                    value = str(value)

                json.update({attr: value})

        return json['id'], dumps(json)

    @staticmethod
    def __is_table_name(attr):
        if not attr.startswith('__t'):
            return False

        return True
