from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.services import database
from app.services import redis
from app.services import kafka


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...

    @property
    @abstractmethod
    def redis(self) -> redis.ServiceRedis:
        ...

    @property
    @abstractmethod
    def kafka(self) -> kafka.ServiceKafka:
        ...
