from event_bus import EventBus
from fraud_control import FraudChecker
from gateway_providers import GatewayFactory
from helpers import IdempotencyCache
from middlewares import impodent, retry_in_network_error

idempotency_cache = IdempotencyCache()

class CheckoutFacade():

    def __init__(self, fraud_checker: FraudChecker, event_bus: EventBus):

        self.fraud_checker = fraud_checker
        self.event_bus = event_bus


    @impodent(cache=idempotency_cache)
    @retry_in_network_error()
    def process_checkout(self, amount: float, country: str, 
                         gateway_factory: GatewayFactory, impodency_key: str = None) -> dict:

        res = self.fraud_checker.check_transactions(amount, country)

        if res == 'BLOCKED':
            return {'status': 'rejected', 'reason': 'Fraud Control blocked transaction'}

        client = gateway_factory.create_client()

        res = client.charge(amount)

        if res['status'] == 'success':
            self.event_bus.notify('payment_success', {'amount': amount, 'country': country})

        return res
    