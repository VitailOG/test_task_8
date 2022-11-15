import redis

from typing import Callable, Any

from fastapi import FastAPI


def event_wrapper(app: FastAPI) -> Callable[[], Any]:
    async def startup_event():
        app.state.redis = redis.StrictRedis()
    return startup_event
