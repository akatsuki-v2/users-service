from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any
from uuid import UUID
from uuid import uuid4

from app.common import logging
from app.common import security
from app.common import validation
from app.common.context import Context
from app.common.errors import ServiceError
from app.models.accounts import AccountUpdate
from app.repositories.accounts import AccountsRepo
from app.repositories.credentials import CredentialsRepo


async def sign_up(ctx: Context,
                  username: str,
                  password: str,
                  email_address: str,
                  country: str) -> Mapping[str, Any] | ServiceError:
    a_repo = AccountsRepo(ctx)
    c_repo = CredentialsRepo(ctx)

    # perform data validation

    if not validation.validate_username(username):
        return ServiceError.ACCOUNTS_INVALID_USERNAME

    if not validation.validate_password(password):
        return ServiceError.ACCOUNTS_INVALID_PASSWORD

    if not validation.validate_email(email_address):
        return ServiceError.ACCOUNTS_EMAIL_ADDRESS_INVALID

    if not validation.validate_country(country):
        return ServiceError.ACCOUNTS_COUNTRY_INVALID

    if await a_repo.fetch_one(email_address=email_address) is not None:
        return ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS

    if await a_repo.fetch_one(username=username) is not None:
        return ServiceError.ACCOUNTS_USERNAME_EXISTS

    transaction = await ctx.db.transaction()

    try:
        account_id = uuid4()
        account = await a_repo.create(account_id=account_id,
                                      username=username,
                                      email_address=email_address,
                                      country=country)

        hashed_password = await security.hash_password(password)

        # create two sets of credentials for the user;
        # allow them to login in via username or email address
        for identifier_type, identifier, passphrase in (
            ("username", username, hashed_password),
            ("email", email_address, hashed_password),
        ):
            credentials_id = uuid4()
            await c_repo.create(credentials_id=credentials_id,
                                account_id=account_id,
                                identifier_type=identifier_type,
                                identifier=identifier,
                                passphrase=passphrase)

    except Exception as exc:  # pragma: no cover
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

    updates = {
        field: value
        for field in AccountUpdate.__fields__
        if (value := kwargs.get(field)) is not None
    }

    if not updates:
        # return the account as-is
        return account

    account = await repo.partial_update(account_id, **updates)
    assert account is not None
    return account


async def delete(ctx: Context, account_id: UUID) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.delete(account_id)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account
