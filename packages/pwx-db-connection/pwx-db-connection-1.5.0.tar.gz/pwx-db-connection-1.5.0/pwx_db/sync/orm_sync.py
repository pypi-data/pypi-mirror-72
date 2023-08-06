from json import dumps
from datetime import datetime


class ORMSync:
    __slots__ = ['__keys', '__json', '__id', '__attrs_to_ignore', '__attrs_to_id']

    __default_ignore = ['__', '_', 'query', 'metadata']

    def __init__(self):
        self.__id = ''
        self.__attrs_to_id = None
        self.__json = {}
        self.__attrs_to_ignore = []

    def __prepare(self, attrs_to_ignore=None, attrs_to_id=None):
        self.__attrs_to_ignore = attrs_to_ignore or []
        self.__attrs_to_id = attrs_to_id or None
        self.__id = ''

    def to_json(self, obj, attrs_to_ignore=None, attrs_to_id=None):
        self.__prepare(attrs_to_ignore, attrs_to_id)
        self.__set_keys(obj)
        self.__generate_json(obj)

        return self.__id, self.__json

    def __set_keys(self, obj):
        self.__keys = [key for key in dir(obj) if not self.__ignore_keys(key, obj)]

    def __ignore_keys(self, key, obj):
        for ignore in self.__default_ignore:
            if key.startswith(ignore):
                return True

        return True if callable(getattr(obj, key)) or self.__attrs_to_ignore.__contains__(key) else False

    def __generate_json(self, obj):
        self.__clear_json()

        for key in self.__keys:
            if isinstance(obj.__getattribute__(key), list):
                continue

            elif isinstance(obj.__getattribute__(key), datetime):
                self.__json.update({key: str(obj.__getattribute__(key))})

            else:
                self.__json.update({key: obj.__getattribute__(key)})

        self.__set_id()
        self.__dumps_json()

    def __dumps_json(self):
        self.__json = dumps(self.__json)

    def __set_id(self):
        if self.__attrs_to_id:
            for att in self.__attrs_to_id:
                if not self.__id:
                    self.__id = self.__json.get(att)

                else:
                    self.__id = f'{self.__id}_{self.__json.get(att)}'

        else:
            self.__id = self.__json.get('id')

    def __clear_json(self):
        if self.__json:
            self.__json = {}
