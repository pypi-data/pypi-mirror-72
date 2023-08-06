from json import loads, dumps
from .pwx_redis import RedisDB


class RedisPWX:

    __slots__ = []

    redis = RedisDB().redis

    def __init__(self):
        pass

    def add(self, collection, key, value):
        self.redis.hset(name=collection, key=key, value=value)

    def add_many(self, collection, values):
        self.redis.hmset(name=collection, mapping=values)

    def get_by_key(self, collection, key):
        result = self.redis.hget(name=collection, key=key)

        if result:
            return self.__loads_result(result)

        return None

    def get_many_by_keys(self, collection, values=None):
        if not isinstance(values, list):
            raise TypeError

        objects = []

        for value in values:
            obj = self.get_by_key(collection, key=value)

            if not obj:
                return None

            objects.append(obj)

        return objects

    def get_by_value(self, collection, attr=None, value=None):
        all_result = self.get_all(collection)

        if all_result:
            for k in all_result:
                values = self.__loads_result(all_result[k])
                if values[attr].__eq__(value):
                    return int(k)

            return None

        else:
            return None

    def get_many_id_by_value(self, collection, attr=None, value=None):
        all_result = self.get_all(collection)

        if all_result:
            result = []

            for k in all_result:
                values = self.__loads_result(all_result[k])
                if values[attr].__eq__(value):
                    result.append(int(k))

            if result:
                return result

            return None

        else:
            return None

    def get_by_values(self, collection, attrs, values):
        if not isinstance(attrs, list) or not isinstance(values, list):
            raise TypeError

        if not len(attrs).__eq__(len(values)):
            raise AssertionError

        all_result = self.get_all(collection=collection)

        if all_result:
            for k in all_result:
                obj_values = self.__loads_result(all_result[k])
                is_return = True

                for i in range(len(attrs)):
                    if not obj_values[attrs[i]].__eq__(values[i]):
                        is_return = False
                        break

                if is_return:
                    return int(k)

            return None

        else:
            return None

    def get_all(self, collection):
        return self.redis.hgetall(name=collection)

    def get_entity_by_value(self, collection, attr=None, value=None):
        all_result = self.get_all(collection)

        if all_result:
            for k in all_result:
                values = self.__loads_result(all_result[k])
                if values[attr] == value:
                    return self.get_by_key(collection=collection, key=int(k))

            return None

        else:
            return None

    def get_entity_by_values(self, collection, attrs, values):
        if not isinstance(attrs, list) or not isinstance(values, list):
            raise TypeError

        if not len(attrs).__eq__(len(values)):
            raise AssertionError

        all_result = self.get_all(collection=collection)

        if all_result:
            for k in all_result:
                obj_values = self.__loads_result(all_result[k])
                is_return = True

                for i in range(len(attrs)):
                    if not obj_values[attrs[i]] == values[i]:
                        is_return = False
                        break

                if is_return:
                    return self.get_by_key(collection=collection, key=int(k))

            return None

        else:
            return None

    def get_many_entities_by_value(self, collection, attr=None, value=None):
        all_result = self.get_all(collection)

        if all_result:
            result = []

            for k in all_result:
                values = self.__loads_result(all_result[k])
                if values[attr].__eq__(value):
                    result.append(self.get_by_key(collection=collection, key=int(k)))

            if result:
                return result

            return None

        else:
            return None

    def get_many_entities_by_values(self, collection, attrs, values):
        if not isinstance(attrs, list) or not isinstance(values, list):
            raise TypeError

        if not len(attrs).__eq__(len(values)):
            raise AssertionError

        all_result = self.get_all(collection=collection)

        if all_result:
            result = []

            for k in all_result:
                is_return = True
                obj_values = self.__loads_result(all_result[k])

                for i in range(len(attrs)):
                    if not isinstance(values[i], list):
                        if not obj_values[attrs[i]] == values[i]:
                            is_return = False
                            break

                    else:
                        for j in values[i]:
                            if obj_values[attrs[i]] == j:
                                is_return = True
                                break
                            else:
                                is_return = False

                if is_return:
                    result.append(obj_values)

            if result:
                return result

            return None

        return None

    def update(self, collection, key, value):
        self.redis.hset(name=collection, key=key, value=dumps(value))

    def delete(self, collection, key):
        self.redis.hdel(collection, key)

    def delete_many(self, collection, *keys):
        self.redis.hdel(collection, *keys)

    @staticmethod
    def __loads_result(result):
        return loads(result)
