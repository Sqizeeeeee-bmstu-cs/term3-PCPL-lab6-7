
from base_interfaces import FraudChecker


class StandardRiskChecker(FraudChecker):

    def __init__(self, max_allowed_amount: float):

        self.max_allowed_amount = max_allowed_amount

    def check_transactions(self, amount: float, _) -> str:

        if amount <= self.max_allowed_amount:
            return "ALLOWED"

        else:
            return "REQUIRED_3DS"
        


class HighRiskZoneChecker(FraudChecker):

    def __init__(self, max_allowed_amount: float, 
                 blocked_countries: list[str]):

        self.max_allowed_amount = max_allowed_amount
        self.blocked_countries = blocked_countries


    def check_transactions(self, amount, country):

        if country in self.blocked_countries:
            return "BLOCKED"

        if amount > self.max_allowed_amount:
            return "BLOCKED"

        else:
            return 'ALLOWED'

