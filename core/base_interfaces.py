
from abc import ABC, abstractmethod


class FraudChecker(ABC):

    @abstractmethod
    def check_transactions(self, amount: float, country: str) -> str:

        pass

