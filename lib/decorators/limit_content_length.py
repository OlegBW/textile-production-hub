from functools import wraps
from flask import request, abort


def limit_content_length(max_size):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            content_length = request.content_length
            if content_length > max_size:
                abort(413)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
