__author__ = 'rey'


class Pagination():
    current_page = 0
    count_all_items = 0
    count_items_on_page = 1
    count_pages = 0

    def __init__(self, count_all_items, current_page, count_items_on_page=None):
        self.count_all_items = int(count_all_items)
        self.current_page = int(current_page)

        if count_items_on_page is not None:
            self.count_items_on_page = int(count_items_on_page)

        self.count_pages = self.calculate_count_pages()

    def calculate_count_pages(self):
        """
        Получение необходимого количества страниц - без раундов и прочего округления. К общему количеству элементов
        прибавим хвост в виде требуемого количества объектов на странице за вычетом одного и поделим на необходимое
        количество элементов на странице - полученный результат при приведенный к инту отбрасывает дробную часть,
        которая будет лишней - останется только чистое количество необходимых страниц.
        """
        return int(float(self.count_all_items + (self.count_items_on_page - 1)) / float(self.count_items_on_page))

    def get_pages(self):
        """
        Вернет словарь из актуальных номеров страниц
        """
        if self.count_pages <= 10:
            # Если общее количество элементов меньше 10
            pages = set(range(1, self.count_pages + 1))
        else:
            # Если элементов больше 10 происходит разбивка на группы
            # первая группа от 1 до 3, следующая от текущей +-2 страницы, последняя группа 3 последние страницы
            pages = (set(range(1, 4))
                     | set(range(max(1, self.current_page - 2), min(self.current_page + 3, self.count_pages + 1)))
                     | set(range(self.count_pages - 2, self.count_pages + 1)))

        return sorted(pages)

    @property
    def start_item(self):
        return int(self.count_items_on_page * self.current_page - (self.count_items_on_page - 1))

    @property
    def end_item(self):
        return int(self.count_items_on_page * self.current_page)

    @property
    def skip_items(self):
        return int(self.start_item - 1)
