from __future__ import annotations

from typing import Any
from typing import Mapping
from uuid import UUID

from app.common.context import Context


class AccountsRepo:
    READ_PARAMS = """\
        rec_id, account_id, username, safe_username, email_address,
        country, status, created_at, updated_at"""

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     account_id: UUID,
                     username: str,
                     email_address: str,
                     country: str) -> Mapping[str, Any] | None:
        query = """\
            INSERT INTO accounts (account_id, username, email_address, country)
                 VALUES (:account_id, :username, :email_address, :country)
        """
        params = {
            "account_id": account_id,
            "username": username,
            "email_address": email_address,
            "country": country,
        }
        rec_id: int = await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
             WHERE rec_id = :rec_id
        """
        params = {"rec_id": rec_id}
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def fetch_one(self, account_id: UUID) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
             WHERE account_id = :account_id
        """
        params = {"account_id": account_id}
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def fetch_all(self) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
        """
        accounts = await self.ctx.db.fetch_all(query)
        return accounts

    async def partial_update(self, account_id: UUID, **updates: Any) -> None:
        ...  # TODO

    async def delete(self, account_id: UUID) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM accounts
             WHERE account_id = :account_id
        """
        params = {"account_id": account_id}
        account = await self.ctx.db.fetch_one(query, params)

        query = """\
            DELETE FROM accounts
                  WHERE account_id = :account_id
        """
        params = {"account_id": account_id}
        await self.ctx.db.execute(query, params)
        return account
