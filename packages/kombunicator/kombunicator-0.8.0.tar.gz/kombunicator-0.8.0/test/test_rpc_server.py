import time
import pytest
import json
from datetime import datetime
from threading import Event

from test import celery_app

from kombunicator import RPCServer


@pytest.mark.timeout(60)
def test_rpc_server_start_stop(conn_param, tmpdir):

    data_processor_name = 'test_processor'
    @celery_app.task(name=data_processor_name)
    def process_request(data):
        data['processed'] = str(datetime.now())
        return data

    test_server_ready = Event()
    test_server = RPCServer(
        connection_parameter=conn_param,
        listening_key='rpc_test_server_key',
        celery_app=celery_app,
        processing_task_name=data_processor_name,
        ready=test_server_ready
    )

    test_server.start()
    test_server_ready.wait()

    # check if server actually works here via publisher

    test_server.stop()

    # test that server is not running anymore


@pytest.mark.timeout(60)
def test_rpc_server_message_processing(tmpdir, conn_param):

    f_name = f'{tmpdir}/rpc_file.json'

    # this task is registered inside the rpc_server file since the celery app is finalized there
    data_processor_write_to_file = 'write_to_file_processor'

    test_server_ready = Event()
    test_server = RPCServer(
        connection_parameter=conn_param,
        listening_key='rpc_test_server_key',
        celery_app=celery_app,
        processing_task_name=data_processor_write_to_file,
        ready=test_server_ready
    )

    payload = {'body_key': 'body_value', 'f_name': f_name}
    headers = {}
    properties = {}
    test_server._on_message(payload, headers, properties)
    time.sleep(2)

    with open(f_name) as fh:
        received_message = json.loads(fh.read())

    assert received_message.get('processed')
    assert received_message.get('body_key') == payload["body_key"]
