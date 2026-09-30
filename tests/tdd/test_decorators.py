import os
import sys
from unittest.mock import MagicMock

import pytest

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
CORE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "core"))

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CORE_DIR)

from middlewares import retry_in_network_error  # type: ignore


def test_retry_decorator_success_after_failures():
    """Проверяем, что декоратор делает повторные попытки при сетевой ошибке

    и возвращает результат, если одна из попыток удалась."""

    # Создаем мок функции, которую будем оборачивать декоратором
    mock_func = MagicMock()

    # Настраиваем её так, чтобы при первых двух вызовах она падала с ConnectionError,
    # а на третий вызов возвращала "success"
    mock_func.side_effect = [ConnectionError, ConnectionError, "success"]

    # Оборачиваем наш мок декоратором (ставим delay=0, чтобы тесты не ждали и прошли мгновенно)
    @retry_in_network_error(retries=3, delay=0.0)
    def decorated_function():
        return mock_func()

    # Вызываем декорированную функцию
    result = decorated_function()

    # Проверяем результаты
    assert result == "success"
    # Убеждаемся, что функция внутри была вызвана ровно 3 раза
    assert mock_func.call_count == 3


def test_retry_decorator_raises_exception_on_exhaustion():
    """Проверяем, что если все попытки исчерпаны, декоратор пробрасывает ConnectionError."""

    mock_func = MagicMock()
    # Функция всегда падает
    mock_func.side_effect = ConnectionError

    @retry_in_network_error(retries=3, delay=0.0)
    def decorated_function():
        return mock_func()

    # Проверяем, что вызывая функцию, мы действительно ловим ConnectionError
    with pytest.raises(ConnectionError) as exc_info:
        decorated_function()

    assert "could not connect to resource" in str(exc_info.value)
    assert mock_func.call_count == 3
