from __future__ import annotations

from typing import Any
from typing import Mapping
from uuid import UUID

from app.common.context import Context
from app.models import Status


class AccountsRepo:
    READ_PARAMS = """\
        account_id, username, safe_username, email_address, country,
        status, created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     username: str,
                     email_address: str,
                     country: str,
                     status: Status = Status.ACTIVE) -> Mapping[str, Any]:
        query = f"""\
            INSERT INTO accounts (username, email_address, country, status)
                 VALUES (:username, :email_address, :country, :status)
              RETURNING {self.READ_PARAMS}
        """
        params = {
            "username": username,
            "email_address": email_address,
            "country": country,
            "status": status,
        }
        account = await self.ctx.db.fetch_one(query, params)
        assert account is not None
        return account

    async def fetch_one(self, account_id: int | None = None,
                        username: str | None = None,
                        email_address: str | None = None,
                        country: str | None = None,
                        status: Status | None = Status.ACTIVE) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
             WHERE account_id = COALESCE(:account_id, account_id)
               AND username = COALESCE(:username, username)
               AND email_address = COALESCE(:email_address, email_address)
               AND country = COALESCE(:country, country)
               AND status = COALESCE(:status, status)
        """
        params = {
            "account_id": account_id,
            "username": username,
            "email_address": email_address,
            "country": country,
            "status": status,
        }
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def fetch_all(self, country: str | None = None,
                        status: Status | None = Status.ACTIVE
                        ) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
             WHERE country = COALESCE(:country, country)
               AND status = COALESCE(:status, status)
        """
        params = {"country": country, "status": status}
        accounts = await self.ctx.db.fetch_all(query, params)
        return accounts

    async def partial_update(self, account_id: int, **updates: Any
                             ) -> Mapping[str, Any] | None:
        if not updates:
            return None

        query = f"""\
            UPDATE accounts
               SET {", ".join(f"{k} = :{k}" for k in updates)},
                   updated_at = CURRENT_TIMESTAMP
             WHERE account_id = :account_id
         RETURNING {self.READ_PARAMS}
        """
        params = {"account_id": account_id, **updates}
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def delete(self, account_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE accounts
               SET status = 'deleted',
                   updated_at = CURRENT_TIMESTAMP
             WHERE account_id = :account_id
         RETURNING {self.READ_PARAMS}
        """
        params = {"account_id": account_id}
        account = await self.ctx.db.fetch_one(query, params)
        return account
