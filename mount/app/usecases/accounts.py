from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any
from uuid import UUID
from uuid import uuid4

from app.common import logging
from app.common import validation
from app.common.context import Context
from app.common.errors import ServiceError
from app.models.accounts import AccountUpdate
from app.repositories.accounts import AccountsRepo
from app.repositories.credentials import CredentialsRepo


async def signup(ctx: Context,
                 username: str,
                 password: str,
                 email_address: str,
                 country: str) -> Mapping[str, Any] | ServiceError:
    a_repo = AccountsRepo(ctx)
    c_repo = CredentialsRepo(ctx)

    # TODO: should validation have more specific errors?

    if not validation.validate_email(email_address):
        return ServiceError.ACCOUNTS_CANNOT_CREATE

    transaction = await ctx.db.transaction()

    try:
        account_id = uuid4()
        account = await a_repo.create(account_id=account_id,
                                      username=username,
                                      email_address=email_address,
                                      country=country)
        if account is None:
            await transaction.rollback()
            return ServiceError.ACCOUNTS_CANNOT_CREATE

        credentials_id = uuid4()
        credentials = await c_repo.create(credentials_id=credentials_id,
                                          account_id=account_id,
                                          identifier_type="email",
                                          identifier=email_address,
                                          passphrase=password)
        if credentials is None:
            await transaction.rollback()
            return ServiceError.CREDENTIALS_CANNOT_CREATE

    except Exception as exc:
        await transaction.rollback()
        logging.error("Unable to create account:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_CANNOT_CREATE
    else:
        await transaction.commit()

    return account


async def fetch_one(ctx: Context, account_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.fetch_one(account_id)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_all(ctx: Context) -> list[Mapping[str, Any]]:
    repo = AccountsRepo(ctx)
    accounts = await repo.fetch_all()
    return accounts


async def partial_update(ctx: Context,
                         account_id: UUID,
                         **kwargs: Any | None) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.fetch_one(account_id)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    updates = {}

    for field in AccountUpdate.__fields__:
        value = kwargs[field]
        if value is not None and value != account[field]:
            updates[field] = value

    if not updates:
        # TODO: should we return an error here?
        return account

    updated = await repo.partial_update(account_id, **updates)
    assert updated is not None

    return updated


async def delete(ctx: Context, account_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.fetch_one(account_id)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    await repo.delete(account_id)
    return account
