import pytest

import kombunicator
from kombunicator.BaseConsumer import BaseConsumer
from kombunicator.ConsumerConfigurator import ConsumerConfigurator

from test import get_random_string


def test_base_consumer_not_implemented():
    consumer = BaseConsumer()
    with pytest.raises(NotImplementedError):
        consumer.process_message({}, {}, {})


def test_consumer_configurator_not_implemented():

    with pytest.raises(NotImplementedError):
        ConsumerConfigurator()

    with pytest.raises(NotImplementedError):
        ConsumerConfigurator.message_handler({}, {}, {})


def test_consumer_configurator_exchange_naming(conn_param):

    exchange_name = 'amq.this_should_throw_exception.exchange'
    binding_keys = ['bk_error']

    # try to bind to an amq. exchange directly
    with pytest.raises(ValueError):
        class InvalidExchangeConsumer(ConsumerConfigurator):
            def configure(self):
                self.connection_parameter = conn_param
                self.exchange_name = exchange_name
                self.binding_keys = binding_keys
                self.consumer_type = 'topic'
                self.q_unique = get_random_string()
                self.accept = ['json']

            @classmethod
            def message_handler(cls, payload, headers, properties):
                pass

        kombunicator.register_message_consumer(InvalidExchangeConsumer)

    exchange_name = 'valid_exchange_name'

    # try and unknown consumer type
    with pytest.raises(ValueError):
        class InvalidTypeConsumer(ConsumerConfigurator):
            def configure(self):
                self.connection_parameter = conn_param
                self.exchange_name = exchange_name
                self.binding_keys = binding_keys
                self.consumer_type = 'unknown_consumer_type'
                self.q_unique = get_random_string()
                self.accept = ['json']

            @classmethod
            def message_handler(cls, payload, headers, properties):
                pass

        kombunicator.register_message_consumer(InvalidTypeConsumer)
