"""Класс-помощник для подсчета значений необходимых для корректной реализации постраничной навигации."""


class Pagination:
    """Pagination на основе переданных данных, через свои методы, может вернуть значения которые необходимы для выборки записей.

    :type current_page: int
    :type count_all_items: int
    :type count_items_on_page: int
    :type count_pages: int
    """

    current_page = 0
    count_all_items = 0
    count_items_on_page = 1
    count_pages = 0

    def __init__(self, count_all_items: int, current_page: int, count_items_on_page: int = None):
        """Создание класса Pagination и передача основных необходимых данных для расчетов.

        :param count_all_items: Количество всех объектов;
        :type count_all_items: int
        :param current_page: Номер текущей страницы;
        :type current_page: int
        :param count_items_on_page: Количество объектов на странице;
        :type count_items_on_page: int
        """
        self.count_all_items = count_all_items
        self.current_page = current_page if current_page > 0 else 1

        if count_items_on_page is not None:
            self.count_items_on_page = count_items_on_page

        self.count_pages = self.calculate_count_pages()

    def calculate_count_pages(self) -> int:
        """Получение необходимого количества страниц - без раундов и прочего округления.

        К общему количеству элементов прибавим хвост в виде требуемого количества объектов на странице за вычетом одного
        (на последней странице может оказаться один единственный элемент)
        и поделим на необходимое количество элементов на странице - полученный результат при приведенный к инту отбрасывает дробную часть,
        которая будет лишней - останется только чистое количество необходимых страниц.

        :return:
        :rtype: int
        """
        return int(float(self.count_all_items + (self.count_items_on_page - 1)) / float(self.count_items_on_page))

    def get_pages(self) -> dict:
        """Вернет словарь из актуальных номеров страниц.

        :return:
        :rtype: dict
        """
        if self.count_pages <= 10:
            # Если общее количество элементов меньше 10.
            pages = set(range(1, self.count_pages + 1))
        else:
            # Если элементов больше 10 происходит разбивка на группы -
            # первая группа от 1 до 3, следующая от текущей +-2 страницы, последняя группа 3 последние страницы.
            pages = (set(range(1, 4))
                     | set(range(max(1, self.current_page - 2), min(self.current_page + 3, self.count_pages + 1)))
                     | set(range(self.count_pages - 2, self.count_pages + 1)))

        return sorted(pages)

    @property
    def start_item(self) -> int:
        """Вернет порядковый номер первого элемента на текущей странице.

        :return: Количество элементов на страницу * номер текущей страницы - (количество элементов на страницу -1);
        :rtype: int
        """
        return int(self.count_items_on_page * self.current_page - (self.count_items_on_page - 1))

    @property
    def end_item(self) -> int:
        """Вернет порядковый номер последнего элемента на текущей странице.

        :return: Количество элементов на страницу * номер текущей страницы;
        :rtype: int
        """
        return int(self.count_items_on_page * self.current_page)

    @property
    def skip_items(self) -> int:
        """Вернет количество элементов которое необходимо пропустить для выборки на текущей странице.

        :return: Порядковй номер первого элемента на странице -1;
        :rtype: int
        """
        return int(self.start_item - 1)
