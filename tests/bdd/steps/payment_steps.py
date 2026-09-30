import os
import sys

from behave import given, then, when

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../.."))
CORE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, "core"))

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CORE_DIR)

from checkout_service import CheckoutFacade  # type: ignore
from event_bus import EventBus  # type: ignore
from fraud_control import HighRiskZoneChecker, StandardRiskChecker  # type: ignore
from gateway_providers import (  # type: ignore
    PayPalGatewayFactory,
    RevolutGatewayFactory,
    StripeGatewayFactory,
)


@given('систему проверки фрода с лимитом {limit:f} евро')
def step_given_standard_fraud(context, limit):
    context.fraud_checker = StandardRiskChecker(max_allowed_amount=limit)

@given('систему проверки фрода с лимитом {limit:f} евро и черным списком "{countries}"')
def step_given_high_risk_fraud(context, limit, countries):
    blocked_list = [c.strip() for c in countries.split(",")]
    context.fraud_checker = HighRiskZoneChecker(max_allowed_amount=limit, blocked_countries=blocked_list)

@given('пустую шину событий')
def step_given_event_bus(context):
    context.event_bus = EventBus()

@when('пользователь из страны "{country}" совершает покупку на сумму {amount:f} евро через фабрику "{provider}"')
def step_when_process_checkout(context, country, amount, provider):
    # Выбираем нужную фабрику по текстовому имени
    if provider == "Stripe":
        factory = StripeGatewayFactory()
    elif provider == "PayPal":
        factory = PayPalGatewayFactory()
    else:
        factory = RevolutGatewayFactory()
        
    facade = CheckoutFacade(fraud_checker=context.fraud_checker, event_bus=context.event_bus)
    
    # Запускаем реальный процесс!
    context.result = facade.process_checkout(
        amount=amount,
        country=country,
        gateway_factory=factory,
        impodency_key=f"bdd-key-{amount}"
    )

@then('платеж должен завершиться со статусом "{status}"')
def step_then_assert_success_status(context, status):
    assert context.result['status'] == status

@then('в ответе провайдером должен быть указан "{provider}"')
def step_then_assert_provider(context, provider):
    assert context.result['provider'] == provider

@then('платеж должен быть отклонен со статусом "{status}"')
def step_then_assert_rejected_status(context, status):
    assert context.result['status'] == status
