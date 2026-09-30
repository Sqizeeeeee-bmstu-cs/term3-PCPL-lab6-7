import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../.."))
CORE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "core"))

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CORE_DIR)


from fraud_control import HighRiskZoneChecker, StandardRiskChecker  # type: ignore


def test_standard_risk_checker():
    """Проверяем лимиты для обычной стратегии."""
    # Инициализируем чекер с лимитом 5000
    checker = StandardRiskChecker(max_allowed_amount=5000.0)

    # Если сумма меньше или равна лимиту — должно быть ALLOWED
    assert checker.check_transactions(1000.0, "US") == "ALLOWED"
    assert checker.check_transactions(5000.0, "US") == "ALLOWED"

    # Если сумма больше лимита — должно быть REQUIRED_3DS
    assert checker.check_transactions(5000.01, "US") == "REQUIRED_3DS"


def test_high_risk_zone_checker_blocked_countries():
    """Проверяем блокировку опасных стран независимо от суммы."""
    checker = HighRiskZoneChecker(max_allowed_amount=10000.0, blocked_countries=["CN", "IR"])

    # Любая сумма в заблокированной стране должна быть BLOCKED
    assert checker.check_transactions(10.0, "CN") == "BLOCKED"
    assert checker.check_transactions(50000.0, "IR") == "BLOCKED"


def test_high_risk_zone_checker_amount_limits():
    """Проверяем лимиты сумм для неопасных стран."""
    checker = HighRiskZoneChecker(max_allowed_amount=10000.0, blocked_countries=["CN", "IR"])

    # В безопасной стране маленькая сумма разрешена
    assert checker.check_transactions(5000.0, "US") == "ALLOWED"

    # В безопасной стране сумма выше лимита блокируется
    assert checker.check_transactions(10001.0, "US") == "BLOCKED"
