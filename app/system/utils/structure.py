

import json


class Structure():

    _data = None

    def __init__(self):
        """
        Инициализация определяет корректность структуры данных - в виде словаря.
        Изначально данные повтоярют пустую структуру.

        :return:
        """
        self._data = self.get_structure()
        assert isinstance(self._data, dict)

    def __iter__(self):
        """

        :return:
        """
        return self._ripper(self._data)

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        for i in self._ripper(self._data, set_key=key, set_value=value):
            if i == key:
                return True
        return False

    def __getitem__(self, item):
        # for i in self._ripper(self.get_structure(), set_key=item):
        #     if i == item:
        #         return True
        return False

    def get_structure(self):
        """

        :return:
        """
        return {}

    def get_data(self):
        """
        Вернет весь массив данных.

        :return:
        """
        return self._data

    def fill_by_method(self, method):
        """

        :param method:
        :return:
        """
        # print(self.get_structure())
        for i, k in self._ripper(self._data, setter=method):
            pass

    def fill_by_data(self, data):
        """

        :param data:
        :return:
        """
        for key, value in data.items():
            for i, k in self._ripper(self._data, set_key=key, set_value=value):
                pass
        return self

    def _ripper(self, structure, prefix='', set_key=None, set_value=None, setter=None):
        """
        Метод рекурсивного обхода структуры и преобразования массива данных

        :param structure:
        :param prefix:
        :param set_key:
        :param set_value:
        :param setter:
        :return:
        """
        # print(structure)
        for key, value in structure.items():
            # print(key)
            # print(value)
            if isinstance(value, dict):
                for i in self._ripper(value, key + '.', set_key, set_value, setter):
                    yield prefix + i, 6
            elif isinstance(value, list):
                j = 0
                for item in value:
                    for i in self._ripper(item, key + '[' + str(j) + '].', set_key, set_value, setter):
                        yield prefix + i, 5
                    j = j + 1
            else:
                current_key = prefix + key

                if setter is not None:
                    try:
                        set_key = current_key
                        set_value = setter(current_key)
                    except:
                        continue

                if set_key is not None:
                    if set_key == current_key:
                        if set_value is not None:
                            structure[key] = set_value
                        else:
                            yield value, 9

                yield current_key, 7

    def get_json(self):
        return json.dumps(self._data)