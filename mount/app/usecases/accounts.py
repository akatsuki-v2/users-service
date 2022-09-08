from __future__ import annotations

import traceback
from typing import Any
from typing import Mapping
from uuid import uuid4

from app.common import logging
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.accounts import AccountsRepo


async def create_account_with_credentials(ctx: Context,
                                          username: str,
                                          password: str,
                                          email_address: str,
                                          country: str) -> Mapping[str, Any] | ServiceError:
    repo = AccountsRepo(ctx)

    # TODO: validate input data

    txn = await ctx.db.txn()

    try:
        account_id = uuid4()
        account = await repo.create(account_id=account_id,
                                    username=username,
                                    email_address=email_address,
                                    country=country)
        if account is None:
            await txn.rollback()
            return ServiceError.ACCOUNTS_CANNOT_CREATE

    except Exception as exc:
        await txn.rollback()
        logging.error("Unable to create account:", error=exc)
        logging.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_CANNOT_CREATE
    else:
        await txn.commit()

    return account
