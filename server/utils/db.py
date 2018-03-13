"""Дополнительные классы для организации устойчивости архитектуры."""


class DocumentDomain:
    """Интерфейс для упрощенной (де)сериализации доменных объектов и документов в БД."""

    def to_document(self):
        """Приведет доменную сущность к словарю пригодному для работы в БД."""
        raise NotImplementedError()

    @classmethod
    def from_document(cls, document):
        """Извлечет из документа БД информацию и по ней создаст объект доменной сущности."""
        raise NotImplementedError()


class Repository:

    def for_insert(self, domain_entity: DocumentDomain) -> dict:
        """Подготовит объект доменной сущности для вставки в БД."""
        document = domain_entity.to_document()
        try:
            # Перед вставкой удаляется ключ _id для его корректной автоматической генерации.
            del document["_id"]
        except KeyError:
            pass
        return document
