"""Утилитарные функции для работы на слое GraphQL."""


def need_auth(func):
    """Требует наличие в контексте ключа 'current_user' или выбросит исключение."""
    def inner(root, info, *args, **kwargs):
        if info.context.get("current_user") is None:
            raise Exception("Доступ через приватную точку доступа")
        return func(root, info, *args, **kwargs)

    return inner
