from abc import ABC, abstractmethod
from typing import Any


class PaymentClient(ABC):

    @abstractmethod
    def charge(self, amount: float) -> dict[str, Any]:
        pass


class WebhookValidator(ABC):

    @abstractmethod
    def validate(self, payload: dict[any], signature: str) -> bool:
        pass

class GatewayFactory(ABC):

    @abstractmethod
    def create_client(self) -> PaymentClient:
        pass

    @abstractmethod
    def create_validator(self) -> WebhookValidator:
        pass

class StripePaymentClient(PaymentClient):

    def charge(self, amount):
        return {'provider': 'stripe', 'status': 'success', 'amount': amount}

class StripeWebhookValidator(WebhookValidator):

    def validate(self, payload, signature):
        return True

class StripeGatewayFactory(GatewayFactory):

    def create_client(self):
        return StripePaymentClient()

    def create_validator(self):
        return StripeWebhookValidator()

# --------------------------------------------


class PayPalPaymentClient(PaymentClient):

    def charge(self, amount):
        return {'provider': 'paypal', 'status': 'success', 'amount': amount}

class PayPalWebhookValidator(WebhookValidator):

    def validate(self, payload, signature):
        return True

class PayPalGatewayFactory(GatewayFactory):

    def create_client(self):
        return PayPalPaymentClient()

    def create_validator(self):
        return PayPalWebhookValidator()

# --------------------------------------------

class RevolutPaymentClient(PaymentClient):

    def charge(self, amount):
        return {'provider': 'revolut', 'status': 'success', 'amount': amount}

class RevolutWebhookValidator(WebhookValidator):

    def validate(self, payload, signature):
        return True

class RevolutGatewayFactory(GatewayFactory):

    def create_client(self):
        return RevolutPaymentClient()

    def create_validator(self):
        return RevolutWebhookValidator()
    