

def need_auth(func):
    def inner(root, args, context, info):
        if context["current_user"] is None:
            raise Exception("Доступ через приватную точку доступа")
        return func(root, args, context, info)

    return inner