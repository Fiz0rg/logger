def wrap_error(err_class, err_message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except err_class:
                raise
            except Exception as err:
                raise err_class(msg=err_message) from err

        return wrapper

    return decorator
