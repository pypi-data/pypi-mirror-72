from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from skywalking import config, agent, Layer, Component
from skywalking.trace import tags
from skywalking.trace.carrier import Carrier
from skywalking.trace.context import get_context
from skywalking.trace.tags import Tag


class SanicSkywalingMiddleware(object):
    def __init__(self, app: Sanic,
                 service: str = None,
                 instance: str = None,
                 collector: str = None,
                 protocol_type: str = 'grpc',
                 token: str = None):
        """
        :param app: Sanic app instance
        :param service: Skywalking Service Name
        :param instance: Skywalking Instance
        :param collector: Skywalking Collector Address
        :param protocol_type: Skywalking protocol type, default to grpc
        :param token: Skywalking authentication token
        """
        self._app = app
        # initialize skywalking agent
        config.init(service, instance, collector, protocol_type, token)
        agent.start()

        if self._app:
            @app.middleware("request")
            def before_request_tracing(request: Request):
                carrier = Carrier()
                for item in carrier:
                    item.val = request.headers.get(item.key.capitalize(), None)
                context = get_context()
                span = context.new_entry_span(op=request.path, carrier=carrier)
                span.start()
                span.layer = Layer.Http
                span.component = Component.General
                span.peer = '%s:%s' % request.socket
                span.tag(Tag(key=tags.HttpMethod, val=request.method))
                request.ctx.sw_span = span

            @app.middleware("response")
            def after_request_tracing(request: Request, response: HTTPResponse):
                if hasattr(request.ctx, 'sw_span') and request.ctx.sw_span:
                    request.ctx.sw_span.stop()
                return response

            @app.exception(BaseException)
            def exception_tracing(request: Request, exception: Exception):
                if exception is not None and hasattr(request.ctx, 'sw_span') and request.ctx.sw_span:
                    request.ctx.sw_span.raised()
