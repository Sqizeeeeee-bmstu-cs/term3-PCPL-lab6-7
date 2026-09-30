import os
import sys
from unittest.mock import MagicMock

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
CORE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "core"))

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CORE_DIR)

from checkout_service import CheckoutFacade  # type: ignore


def test_checkout_blocked_by_fraud():

    # MagicMock — это умный робот. Мы можем приказать ему возвращать всё что угодно.
    mock_fraud = MagicMock()
    mock_bus = MagicMock()
    mock_factory = MagicMock()

    # Настраиваем мок фрода: говорим ему, что при вызове метода check_transactions
    # он должен вернуть строку 'BLOCKED'
    mock_fraud.check_transactions.return_value = "BLOCKED"

    # Наш Фасад думает, что работает с настоящими сервисами, но это наши роботы
    facade = CheckoutFacade(fraud_checker=mock_fraud, event_bus=mock_bus)

    result = facade.process_checkout(
        amount=500.0,
        country="CN",
        gateway_factory=mock_factory,
        impodency_key="unique-key-1",
    )

    # Проверяем, что Фасад вернул правильный словарь с отказом
    assert result["status"] == "rejected"
    assert result["reason"] == "Fraud Control blocked transaction"

    # Проверяем, что Фасад ДЕЙСТВИТЕЛЬНО вызвал проверку фрода с нашими параметрами
    mock_fraud.check_transactions.assert_called_once_with(500.0, "CN")

    # Проверяем, что Фасад НЕ СТАЛ вызывать создание клиента в фабрике (ведь фрод заблокировал платеж)
    mock_factory.create_client.assert_not_called()

    # Проверяем, что в шину событий ничего НЕ отправлялось
    mock_bus.notify.assert_not_called()
