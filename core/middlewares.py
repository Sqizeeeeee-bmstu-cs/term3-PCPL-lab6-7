import time
from functools import wraps
from typing import Any, Callable

from helpers import IdempotencyCache


def retry_in_network_error(retries: int = 3, 
                           delay: float = 0.1):

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            for _ in range(retries):

                try:

                    result = func(*args, **kwargs)

                    if result:
                        return result

                except ConnectionError:

                    time.sleep(delay)

            raise ConnectionError('could not connect to resource')

        return wrapper

    return decorator


def impodent(cache: IdempotencyCache):

    def decorator(func: Callable[..., Any]):

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):

            impodency_key = kwargs.get('impodency_key', None)

            if impodency_key is None:

                return func(*args, **kwargs)

            cached_result = cache.get(impodency_key)

            if cached_result is not None:
                return cached_result

            result = func(*args, **kwargs)

            cache.set(impodency_key, result)

            return result

        return wrapper

    return decorator


