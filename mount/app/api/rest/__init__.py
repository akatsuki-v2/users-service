from __future__ import annotations

from app.common import logging
from fastapi import FastAPI


def init_db(api: FastAPI) -> None:
    @api.on_event("startup")
    async def startup_db():
        logging.info("Starting up the database")

    @api.on_event("shutdown")
    async def shutdown_db():
        logging.info("Shutting down the database")


def init_routes(api: FastAPI) -> None:
    from .v1 import router as v1_router

    api.include_router(v1_router, prefix="/v1")


def init_api():
    api = FastAPI()

    init_db(api)
    init_routes(api)

    return api
