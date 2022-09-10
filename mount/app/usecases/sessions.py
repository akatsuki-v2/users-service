from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any
from uuid import UUID
from uuid import uuid4

from app.common import logging
from app.common import security
from app.common.context import Context
from app.common.errors import ServiceError
from app.models.sessions import SessionUpdate
from app.repositories.credentials import CredentialsRepo
from app.repositories.sessions import SessionsRepo


async def log_in(ctx: Context,
                 username: str,
                 password: str,
                 user_agent: str,
                 ) -> Mapping[str, Any] | ServiceError:
    s_repo = SessionsRepo(ctx)
    c_repo = CredentialsRepo(ctx)

    credentials = await c_repo.fetch_one(identifier=username)
    if credentials is None:
        return ServiceError.CREDENTIALS_NOT_FOUND

    account_id = credentials["account_id"]
    hashed_password = credentials["passphrase"]

    if not await security.check_password(password, hashed_password):
        return ServiceError.CREDENTIALS_INCORRECT

    try:
        session_id = uuid4()
        session = await s_repo.create(session_id=session_id,
                                      account_id=account_id,
                                      user_agent=user_agent)
    except Exception as exc:
        logging.error("Unable to create session:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.SESSIONS_CANNOT_CREATE

    return session


async def log_out(ctx: Context, session_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = SessionsRepo(ctx)

    session = await repo.fetch_one(session_id)
    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    await repo.delete(session_id)
    return session


async def partial_update(ctx: Context,
                         session_id: UUID,
                         **kwargs: Any | None) -> Mapping[str, Any] | ServiceError:
    repo = SessionsRepo(ctx)

    updates = {
        field: value
        for field in SessionUpdate.__fields__
        if (value := kwargs.get(field)) is not None
    }

    session = await repo.partial_update(session_id, **updates)
    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    return session
