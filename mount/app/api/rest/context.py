from app.common.context import Context
from app.services import database
from app.services import redis
from app.services import kafka
from fastapi import Request


class RequestContext(Context):
    def __init__(self, request: Request) -> None:
        self.request = request

    @property
    def db(self) -> database.ServiceDatabase:
        return self.request.state.db

    @property
    def redis(self) -> redis.ServiceRedis:
        return self.request.state.redis

    @property
    def kafka(self) -> kafka.ServiceKafka:
        return self.request.state.kafka
