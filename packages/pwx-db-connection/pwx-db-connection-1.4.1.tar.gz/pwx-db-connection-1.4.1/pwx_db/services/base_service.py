from pwx_db import PostgresDB, RedisPWX
from pwx_db.sync import EntitySync
from json import loads, dumps


class BaseService:
    __slots__ = ['_entity', '_name']

    _db = PostgresDB()
    _redis = RedisPWX()

    def __init__(self, name):
        self._name = name
        self.__sync_entity()

    def __sync_entity(self):
        self._entity = EntitySync(name=self._name)
        self._entity.__sync_attrs__()

    def __execute_sql(self, sql, many=False):
        if not many:
            return self._db.execute_query_one(sql=sql)

        return self._db.execute_query_all(sql=sql)

    def _sync_with_redis(self, sql, attrs_id=None):
        result = self.__execute_sql(sql)

        if not result:
            raise ValueError

        value_id, json = self._entity.__to_json__(values=result)

        if attrs_id and isinstance(attrs_id, list):
            value_id = self.__attributes_to_id(attrs_id, json)

        else:
            self.__save_redis(value_id, json)

        return value_id

    def _sync_many_with_redis(self, sql, attrs_id=None):
        results = self.__execute_sql(sql, many=True)

        if not results:
            raise ValueError

        list_ids = []

        for result in results:
            value_id, json = self._entity.__to_json__(values=result)

            if attrs_id and isinstance(attrs_id, list):
                value_id = self.__attributes_to_id(attrs_id, json)

            else:
                self.__save_redis(value_id, json)

            list_ids.append(value_id)

        return list_ids

    def __save_redis(self, value_id, payload):
        self._redis.add(collection=self._name, key=value_id, value=payload)

    def __attributes_to_id(self, attrs_id, json):
        _id = ''

        if isinstance(json, str):
            json = loads(json)

        for attr in attrs_id:
            if not _id:
                _id = json.get(attr)

            else:
                _id = f'{_id}_{json.get(attr)}'

        self.__save_redis(_id, dumps(json))

        return _id

    def _get_sql(self): ...

    def sync(self): ...
