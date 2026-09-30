from abc import ABC, abstractmethod
from typing import List


class EventSubscriber(ABC):

    @abstractmethod
    def update(self, event_type: str, data: dict) -> None:
        pass

class EventBus():

    def __init__(self):
        self._subscribers: {str, List[EventSubscriber]} = {}

    def subscribe(self, event_type: str, subscriber: EventSubscriber) -> None:

        if event_type not in self._subscribers.keys():

            self._subscribers[event_type] = []

        self._subscribers[event_type].append(subscriber)
        return

    def unsubscribe(self, event_type: str, subscriber: EventSubscriber) -> None:

        if event_type in self._subscribers.keys():

            self._subscribers[event_type].remove(subscriber)
        return

    def notify(self, event_type: str, data: dict[str, EventSubscriber]) -> None:

        for subscriber in self._subscribers.get(event_type, []):

            subscriber.update(event_type, data)
        return
