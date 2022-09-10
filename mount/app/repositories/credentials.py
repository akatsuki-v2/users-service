from __future__ import annotations

from typing import Any
from typing import Mapping
from uuid import UUID

from app.common.context import Context
from app.models import Status


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
                     passphrase: str | bytes,
                     ) -> Mapping[str, Any]:
        query = f"""\
            INSERT INTO credentials (credentials_id, account_id,
                                     identifier_type, identifier, passphrase,
                                     status)
                 VALUES (:credentials_id, :account_id, :identifier_type,
                         :identifier, :passphrase, :status)
              RETURNING {self.READ_PARAMS}
        """
        params = {
            "credentials_id": credentials_id,
            "account_id": account_id,
            "identifier_type": identifier_type,
            "identifier": identifier,
            "passphrase": passphrase,
            "status": "active",
        }
        credentials = await self.ctx.db.fetch_one(query, params)
        assert credentials is not None
        return credentials

    async def fetch_one(self, credentials_id: UUID | None = None,
                        identifier: str | None = None
                        ) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
             WHERE credentials_id = COALESCE(:credentials_id, credentials_id)
               AND identifier = COALESCE(:identifier, identifier)
        """
        params = {"credentials_id": credentials_id, "identifier": identifier}
        credentials = await self.ctx.db.fetch_one(query, params)
        return credentials

    async def fetch_all(self, account_id: UUID | None = None,
                        identifier_type: str | None = None,
                        status: Status | None = Status.ACTIVE
                        ) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM credentials
             WHERE account_id = COALESCE(:account_id, account_id)
               AND identifier_type = COALESCE(:identifier_type, identifier_type)
               AND status = COALESCE(:status, status)
        """
        params = {
            "account_id": account_id,
            "identifier_type": identifier_type,
            "status": status,
        }
        all_credentials = await self.ctx.db.fetch_all(query, params)
        return all_credentials

    async def partial_update(self, credentials_id: UUID, **updates: Any) -> Mapping[str, Any] | None:
        assert updates

        query = f"""\
            UPDATE credentials
               SET {", ".join(f"{k} = :{k}" for k in updates)},
                   updated_at = CURRENT_TIMESTAMP
             WHERE credentials_id = :credentials_id
         RETURNING {self.READ_PARAMS}
        """
        params = {"credentials_id": credentials_id, **updates}
        credentials = await self.ctx.db.fetch_one(query, params)
        return credentials

    async def delete(self, resource_id: UUID) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE resources
               SET status = 'deleted',
                   updated_at = CURRENT_TIMESTAMP
             WHERE resource_id = :resource_id
         RETURNING {self.READ_PARAMS}
        """
        params = {"resource_id": resource_id}
        resource = await self.ctx.db.fetch_one(query, params)
        return resource
