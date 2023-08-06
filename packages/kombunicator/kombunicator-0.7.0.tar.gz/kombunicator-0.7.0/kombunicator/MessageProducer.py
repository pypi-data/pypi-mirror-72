from typing import Union

from kombu import Connection
from kombu import Producer
from kombunicator.Exceptions import AMQPConnectionError
from kombunicator.utils import getter_setter
from strongtyping.strong_typing import match_typing
from kombunicator.BusPlugins import PublishPlugin


class MessageProducer:

    @match_typing
    def __init__(self, connection_parameter: dict, plugin: str = None, retry_policy: dict = None):
        """Create a message producer to publish messages
        to a RabbitMQ instance.

        Parameters
        ----------
        connection_parameter:
            Holds the connection parameters to a RabbitMQ instance.
            - 'hostname': `str` Host where RabbitMQ is accessible
            - 'virtual_host': `str` virtual host of RabbitMQ instance
            - 'port': `int` port to RabbitMQ instance
            - 'userid': `str` username
            - 'password': `str` password
        plugin: `str`
            Plugin for modifying the message based on an specific receiver message bus.

        retry_policy:
            To overwrite the default retry policy which is defined in the following way.
            - 'interval_start': 0,
            - 'interval_step': 2,
            - 'interval_max': 30,
            - 'max_retries': 30

        Raises
        ------
        `kombunicator.AMQPConnectionError`
        """
        self.connection_parameter = connection_parameter
        self._retry_policy = retry_policy if retry_policy is not None else {}

        try:
            conn = Connection(**self.connection_parameter)
            conn.connect()
        except (ConnectionRefusedError, AttributeError, TypeError):
            raise AMQPConnectionError('AMQP connection cannot be established.')
        else:
            # when try was successful
            conn.release()

        self.plugin = plugin

    @PublishPlugin()
    @match_typing
    def publish(self, message: Union[dict, str], headers: dict = {}, exchange: str = '',
                routing_key: str = 'default', correlation_id: str = ''):
        """Publish a message to the RabbitMQ instance.

        Parameters
        ----------
        message : `dict` or `str`
            Message to be published
        headers : `dict`
            Mapping of arbitrary headers to pass along
            with the message
        exchange : `str`
            Name of the exchange to publish a message to
        routing_key : `str`
            Queue routing key
        correlation_id : `str`
            correlation ID to match a specific message
        """
        with Connection(**self.connection_parameter) as connection:
            with Producer(connection) as producer:
                producer.publish(
                    body=message,
                    headers=headers,
                    exchange=exchange,
                    routing_key=routing_key,
                    correlation_id=correlation_id,
                    retry_policy=self._retry_policy
                )

    @getter_setter
    @match_typing
    def _retry_policy(self, value: dict = None) -> dict:
        default_retry_policy = {
            'interval_start': 0,
            'interval_step': 2,
            'interval_max': 30,
            'max_retries': 30
        }
        if value is not None:
            new_retry_policy = self.__check_retry_policy_config__(value, default_retry_policy)
            default_retry_policy.update(new_retry_policy)
            self.__retry_policy = default_retry_policy
        return self.__retry_policy

    @staticmethod
    @match_typing
    def __check_retry_policy_config__(new_config_dict: dict, default_retry_pol: dict) -> dict:
        """
        We allow only keys which are existing in our default retry policy dict
        """
        for bad_key in [k for k in new_config_dict.keys() if k not in default_retry_pol.keys()]:
            del new_config_dict[bad_key]
        return new_config_dict
