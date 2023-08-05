# kombunicator

A threaded RabbitMQ message producer/consumer and RPC server/client.

## Installation
Install directly from the GitLab repository  
`$ pip install --user git+https://gitlab.com/mbio/kombunicator.git`

## Usage
Message consumers are threaded. For graceful shutdown of the threads, SIGINT and SIGTERM are captured. The signal handling routine calls the `stop()` method of the threads, which causes the `kombu.ConsumerMixin` to stop consuming and return. Then, all created threads are joined.

### Message consumers
kombunicator provides a thread-wrapped `kombu.ConsumerMixin` where you can register your own message-handler routine.  

```python
import kombunicator

# define connection parameters to your RabbitMQ instance
rabbit_mq_conn_param = {
    'hostname': 'localhost',
    'port': 5672,
    'userid': 'my_username',
    'password': 'my_password'
}

# define a message consumer class, which inherits from
# kombunicator.ConsumerConfigurator
# One must overwrite the configure method and the
# message_handler method with the latter being a static method.
class ExampleConsumer(kombunicator.ConsumerConfigurator):
    def configure(self):
        self.connection_parameter = rabbit_mq_conn_param
        self.consumer_type='topic',
        self.exchange_name = "example_exchange"
        self.binding_keys = ['binding.key.*']
        self.q_unique = "unique_string"
        self.accept = ['json']

    @classmethod
    def message_handler(cls, payload, headers, properties):
        print(payload)


# finally register the message consumer
kombunicator.register_message_consumer(ExampleConsumer)
```

### Message producer
To publish messages to a RabbitMQ instance, kombunicator provides
a MessageProducer class. It is configured with the connection
parameters for RabbitMQ. Then, it can publish messages (either dict or str)
to the RabbitMQ instance.

```python
from kombunicator import MessageProducer


# define connection parameters to your RabbitMQ instance
rabbit_mq_conn_param = {
    'hostname': 'localhost',
    'port': 5672,
    'userid': 'my_username',
    'password': 'my_password'
}


message = {
    "success": True
}


producer = MessageProducer(rabbit_mq_conn_param)
producer.publish(
    message=message,
    routing_key='backend_q'
)
```

### Remote Procedure Call Server
To set up a Remote Procedure Call (RPC) Server a celery application is required.  
The celery application needs to be configured with a `broker` and a `backend`.  
The following example sets up a celery application with a RabbitMQ message broker  
and a Redis result backend. So let's set up `rpc_server.py`:
```python
import celery
import time
from threading import Event
from kombunicator import RPCServer

# message broker configuration 
broker_connection_parameter = {
    'hostname': 'localhost',
    'port': 5672,
    'userid': 'alice',
    'password': 'wonderland'
}
cp = broker_connection_parameter
broker_url = f"amqp://{cp['userid']}:{cp['password']}@{cp['hostname']}:{cp['port']}"


# result backend configuration
backend_connection_parameter = {
    'hostname': 'localhost',
    'port': 6379,
    'password': 'redispass'
}
bp = backend_connection_parameter
backend_url = f"redis://:{bp['password']}@{bp['hostname']}:{bp['port']}/0"

# create the celery application
celery_app = celery.Celery('tasks', broker=broker_url, backend=backend_url)

# note, that we need to include 'kombunicator.tasks' into the celery app
# to add the kombunicator shared tasks to the celery applicaion.
celery_app.conf.update(
    CELERY_BROKER=broker_url,
    CELERY_RESULT_BACKEND=backend_url,
    CELERY_IMPORTS=('rpc_server', 'kombunicator.tasks')
)

### now use celery app to configure RPCServer

# first, we need a celery task to be executed on a received message.
# This task processes the incoming data.
data_processor_name = 'request_processor'
@celery_app.task(name=data_processor_name)
def process_request(data):
    data['processed'] = True
    return data

# then, we setup the server with direct listening_key and 
# the just created message processing task name
is_ready = Event()
server = RPCServer(
    connection_parameter=broker_connection_parameter,
    listening_key='rpc_server_key',
    celery_app=celery_app,
    processing_task_name=data_processor_name,
    ready=is_ready
)
server.start()
is_ready.wait()

while True:
    time.sleep(1)

```

### Remote Procedure Call Clients
To request data from a remote server via RPC, a RPCClient can be used.
A RPCClient will send over a request to a specific listening key of the
server and then spin up a thread, which waits for the answer. This answer
is then processed by the processing routine attached to the RPCClient.

For the client's answer processor there are two options:
  - define a default processor which is called on request return.
  - define a variable processor which can be customized on every request.
```python
from kombunicator import RPCClient

# connection credentials for celery message broker
broker_connection_parameter = {
    'hostname': 'localhost',
    'port': 5672,
    'userid': 'alice',
    'password': 'wonderland'
}

# define processing call function to be executed on the
# data sent by the RPCServer 
def default_answer_processor(data):
    print(data)

### setup a client with a default processor
client = RPCClient(
    connection_parameter=broker_connection_parameter,
    request_key='rpc_server_key',
    default_callback=default_answer_processor
)

request_data = dict(id='abc123')

# now request only the data. When the result returns, the default processor
# is called with received data.
client.request(request_data)


### setup a client with a custom processor
client = RPCClient(
    connection_parameter=broker_connection_parameter,
    request_key='rpc_server_key',
    default_callback=default_answer_processor
)

def custom_answer_processor(data):
    print(data)

request_data = dict(id='abc123')

# Now call the request method with specified callback. Now, the
# custom callback is executed with received data. 
client.request(request_data, callback=custom_answer_processor)
```

### Shutdown consumers
Every consumer thread runs as daemon. Additionally, kombunicator provides the
`kombunicator.shutdown_consumers()` routine. It is recommended to call this
routine on system exit.

kombunicator catches the two system events SIGINT and SIGTERM. On either of
these, `kombunicator.shutdown_consumers()` is called.
