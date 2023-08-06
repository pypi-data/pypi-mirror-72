class CallbackPlugin:

    def __init__(self, plugin=None, **kwargs):
        self.kwargs = kwargs
        self.plugin = plugin

    def __call__(self, function):
        def wrapped_f(payload, headers, properties):
            if not self.plugin:
                return function(payload, headers, properties)
            # C# Rebus can not set properties and therefor the correlation_id will also be expected in the headers and set to properties.
            elif self.plugin == "rebus":
                if not properties:
                    properties = {}
                if not headers.get('correlation_id'):
                    raise ValueError(f'For {self.plugin} plugin the correlation_id field is expected to be present inside the header.')
                if headers['correlation_id'] == self.kwargs["message_correlation_id"]:
                    properties['correlation_id'] = headers['correlation_id']
                    return function(payload, headers, properties)
            else:
                raise ValueError(
                    f'{self.plugin} is not a known messaging plugin.')
        return wrapped_f


class RPCRequestPlugin:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, function):
        def wrapped_f(self, *args, **kwargs):
            if not self.plugin:
                return function(self, *args, **kwargs)
            elif self.plugin == 'rebus':
                if not kwargs.get('headers'):
                    kwargs['headers'] = {}
                # C# Rebus can not set or access properties and therefor the correlation_id will also be expected in the headers.
                kwargs['headers']['correlation_id'] = kwargs.get(
                    "message_correlation_id")
                kwargs['headers']['reply_to'] = kwargs.get("result_queue_name")
                # Rebus Message processing requires a rbs2-content-type header.
                kwargs['headers']['rbs2-content-type'] = "application/json;charset=utf-8"
                return function(self, *args, **kwargs)
            else:
                raise ValueError(
                    f'{self.plugin} is not a known messaging plugin.')
        return wrapped_f


class PublishPlugin:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, function):
        def wrapped_f(self, *args, **kwargs):
            if not self.plugin:
                return function(self, *args, **kwargs)
            elif self.plugin == "rebus":
                if not kwargs.get('headers'):
                    kwargs["headers"] = {}
                # Rebus Message processing requires a rbs2-content-type header.
                kwargs['headers']['rbs2-content-type'] = "application/json;charset=utf-8"
                return function(self, *args, **kwargs)
            else:
                raise ValueError(
                    f'{self.plugin} is not a known messaging plugin.')
        return wrapped_f
