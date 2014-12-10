

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
        return self._data.copy()

    def fill_by_method(self, method):
        """

        :param method:
        :return:
        """
        for i in self._ripper(self._data, setter=method):
            pass

    def fill_from_document(self, model):
        """
        Заполнит объект входящими данными по структуре
        :param data:
        :return:
        """
        self._data = self._filter(model)

    def _filter(self, data):
        """
        Фильтр приходящих данных от запрещенных полей
        например те которые начинаются с _
        :param data:
        :return:
        """
        if isinstance(data, dict):
            new_dict = {}
            for key in data:
                if key[0] != "_":
                    new_dict[key] = self._filter(data[key])
            return new_dict
        elif isinstance(data, list):
            new_list = []
            for value in data:
                new_list.append(self._filter(value))
            return new_list
        return data

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
                # Проход по словарям
                for item_ripper in self._ripper(value, key + '.', set_key, set_value, setter):
                    yield prefix + item_ripper

            elif isinstance(value, list):
                # Проход по плоским спискам - элементы которых скорее всего содержат словари
                number_item = 0
                for item in value:
                    for item_ripper in self._ripper(item, key + '[' + str(number_item) + '].', set_key, set_value, setter):
                        yield prefix + item_ripper
                    number_item = number_item + 1

            else:
                # Просты элементы подвергаются обработке (сравнению, изменению)
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
                            yield value

                yield current_key

    def get_json(self):
        return json.dumps(self._data)