from typing import Callable

from fastapi.routing import APIRoute
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response


class CustomHTTPConnection(HTTPConnection):
    """ For best get instance redis from state FastApi
    """
    @property
    def redis(self):
        return self.scope["app"].state.redis


class CustomRequest(CustomHTTPConnection, Request):
    pass


class CustomRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = CustomRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
