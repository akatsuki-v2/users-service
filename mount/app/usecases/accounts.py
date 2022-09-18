from __future__ import annotations

import traceback
from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from app.common import logging
from app.common import security
from app.common import validation
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.accounts import AccountsRepo
from app.repositories.credentials import CredentialsRepo
from app.repositories.statistics import StatisticsRepo


async def sign_up(ctx: Context,
                  username: str,
                  password: str,
                  email_address: str,
                  country: str) -> Mapping[str, Any] | ServiceError:
    a_repo = AccountsRepo(ctx)
    c_repo = CredentialsRepo(ctx)
    s_repo = StatisticsRepo(ctx)

    # perform data validation

    if not validation.validate_username(username):
        return ServiceError.ACCOUNTS_USERNAME_INVALID

    if not validation.validate_password(password):
        return ServiceError.ACCOUNTS_PASSWORD_INVALID

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
        account = await a_repo.create(username=username,
                                      email_address=email_address,
                                      country=country)
        account_id = account["account_id"]

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

        # create statistics for each game mode for the user
        for mode in (0, 1, 2, 3, 4, 5, 6, 7):
            await s_repo.create(account_id=account_id,
                                game_mode=mode,
                                total_score=0,
                                ranked_score=0,
                                performance=0,
                                play_count=0,
                                play_time=0,
                                accuracy=0.0,
                                max_combo=0,
                                total_hits=0,
                                replay_views=0,
                                xh_count=0,
                                x_count=0,
                                sh_count=0,
                                s_count=0,
                                a_count=0)

    except Exception as exc:  # pragma: no cover
        await transaction.rollback()
        logging.error("Unable to create account:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_CANNOT_CREATE
    else:
        await transaction.commit()

    return account


async def fetch_one(ctx: Context,
                    account_id: int | None = None,
                    username: str | None = None,
                    email_address: str | None = None,
                    country: str | None = None,
                    status: Status | None = Status.ACTIVE) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.fetch_one(account_id=account_id,
                                   username=username,
                                   email_address=email_address,
                                   country=country,
                                   status=status)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_all(ctx: Context, country: str | None = None,
                    status: Status | None = Status.ACTIVE) -> list[Mapping[str, Any]]:
    repo = AccountsRepo(ctx)
    accounts = await repo.fetch_all(country=country,
                                    status=status)
    return accounts


async def partial_update(ctx: Context,
                         account_id: int,
                         **kwargs: Any | None) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    account = await repo.fetch_one(account_id)
    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    updates = {}

    new_username = kwargs.get("username")
    if new_username is not None and new_username != account["username"]:
        if not validation.validate_username(new_username):
            return ServiceError.ACCOUNTS_USERNAME_INVALID

        if await repo.fetch_one(username=new_username) is not None:
            return ServiceError.ACCOUNTS_USERNAME_EXISTS

        updates["username"] = new_username

    new_email_address = kwargs.get("email_address")
    if new_email_address is not None and new_email_address != account["email_address"]:
        if not validation.validate_email(new_email_address):
            return ServiceError.ACCOUNTS_EMAIL_ADDRESS_INVALID

        if await repo.fetch_one(email_address=new_email_address) is not None:
            return ServiceError.ACCOUNTS_EMAIL_ADDRESS_EXISTS

        updates["email_address"] = new_email_address
        updates["email_address_verification_time"] = None

    new_country = kwargs.get("country")
    if new_country is not None and new_country != account["country"]:
        if not validation.validate_country(new_country):
            return ServiceError.ACCOUNTS_COUNTRY_INVALID

        updates["country"] = new_country

    new_status = kwargs.get("status")
    if new_status is not None and new_status != account["status"]:
        updates["status"] = new_status

    if not updates:
        # return the account as-is
        return account

    account = await repo.partial_update(account_id, **updates)
    assert account is not None
    return account


async def delete(ctx: Context, account_id: int) -> Mapping[str, Any] | ServiceError:
    a_repo = AccountsRepo(ctx)
    c_repo = CredentialsRepo(ctx)
    s_repo = StatisticsRepo(ctx)

    transaction = await ctx.db.transaction()

    try:
        account = await a_repo.delete(account_id)
        if account is None:
            return ServiceError.ACCOUNTS_NOT_FOUND

        all_active_credentials = await c_repo.fetch_all(account_id=account_id,
                                                        status=Status.ACTIVE)
        for active_credentials in all_active_credentials:
            credentials = await c_repo.delete(active_credentials["credentials_id"])
            assert credentials is not None

        for mode in (0, 1, 2, 3, 4, 5, 6, 7):
            statistics = await s_repo.delete(account_id=account_id, game_mode=mode)
            assert statistics is not None

    except Exception as exc:  # pragma: no cover
        await transaction.rollback()
        logging.error("Unable to delete account:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_CANNOT_DELETE
    else:
        await transaction.commit()

    return account
