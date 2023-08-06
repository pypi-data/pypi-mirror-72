
import uuid

from kombu import Exchange, Queue, binding
from strongtyping.strong_typing import match_typing

from kombunicator.BaseConsumer import BaseConsumer


class FanoutConsumer(BaseConsumer):

    @match_typing
    def __init__(self, connection, exchange_name: str, binding_keys: list, accept: list = ['json']):
        super().__init__()
        self.connection = connection
        self.exchange_name = exchange_name
        self.binding_keys = binding_keys
        self.accept = accept

        self.exchange = Exchange(self.exchange_name, type='fanout')
        self.q_bindings = [binding(self.exchange, routing_key=key) for key in self.binding_keys]

        self.queue = Queue(
            name=uuid.uuid4().hex,
            exchange=self.exchange,
            bindings=self.q_bindings,
            auto_delete=True,
            exclusive=True,
            expires=2 * 30 * 24 * 60 * 60
        )
