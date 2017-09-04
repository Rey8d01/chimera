"""Утилитарные функции для работы на слое GraphQL."""


def need_auth(func):
    """Требует наличие в контексте ключа 'current_user' или выбросит исключение."""
    def inner(root, args, context, info):
        if context["current_user"] is None:
            raise Exception("Доступ через приватную точку доступа")
        return func(root, args, context, info)

    return inner
