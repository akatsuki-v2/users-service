from __future__ import annotations

from typing import Any
from typing import Mapping
from uuid import UUID

from app.common.context import Context


class CredentialsRepo:
    READ_PARAMS = """\
        rec_id, credentials_id, account_id, identifier_type, identifier,
        passphrase, status, created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     credentials_id: UUID,
                     account_id: UUID,
                     identifier_type: str,
                     identifier: str,
                     passphrase: str,
                     ) -> Mapping[str, Any] | None:
        query = """\
            INSERT INTO credentials (credentials_id, account_id,
                                     identifier_type, identifier, passphrase)
                 VALUES (:credentials_id, :account_id, :identifier_type,
                         :identifier, :passphrase)
        """
        params = {
            "credentials_id": credentials_id,
            "account_id": account_id,
            "identifier_type": identifier_type,
            "identifier": identifier,
            "passphrase": passphrase,
        }
        rec_id: int = await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
             WHERE rec_id = :rec_id
        """
        params = {"rec_id": rec_id}
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def fetch_one(self, credentials_id: UUID) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
             WHERE credentials_id = :credentials_id
        """
        params = {"credentials_id": credentials_id}
        account = await self.ctx.db.fetch_one(query, params)
        return account

    async def fetch_all(self) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
        """
        all_credentials = await self.ctx.db.fetch_all(query)
        return all_credentials

    async def partial_update(self, credentials_id: UUID, **updates: Any) -> None:
        ...  # TODO

    async def delete(self, credentials_id: UUID) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
             WHERE credentials_id = :credentials_id
        """
        params = {"credentials_id": credentials_id}
        account = await self.ctx.db.fetch_one(query, params)

        query = """\
            DELETE FROM credentials
                  WHERE credentials_id = :credentials_id
        """
        params = {"credentials_id": credentials_id}
        await self.ctx.db.execute(query, params)
        return account
