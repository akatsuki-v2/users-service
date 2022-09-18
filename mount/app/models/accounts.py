from __future__ import annotations

from datetime import datetime

from . import BaseModel
from . import Status


# NOTE: the `country` field is iso-3166-1 alpha-2


class SignupForm(BaseModel):
    username: str
    password: str
    email_address: str
    country: str


class Account(BaseModel):
    account_id: int
    username: str
    safe_username: str  # NOTE: generated column
    email_address: str
    country: str

    status: Status
    created_at: datetime
    updated_at: datetime


class AccountUpdate(BaseModel):
    username: str | None
    email_address: str | None
    country: str | None

    # private endpoint feature
    # not to be exposed to users
    status: Status | None
