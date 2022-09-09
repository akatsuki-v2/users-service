import pytest
from app.common.context import Context
from app.common.errors import ServiceError
from app.usecases import accounts

# https://docs.pytest.org/en/7.1.x/reference/reference.html#globalvar-pytestmark
pytestmark = pytest.mark.asyncio


async def test_should_pass(ctx: Context):
    assert ctx is not None


async def test_should_signup(ctx: Context):
    username = "cmyui"
    password = "lol123"
    email_address = "cmyuiosu@gmail.com"
    country = "CA"
    account = await accounts.signup(ctx,
                                    username=username,
                                    password=password,
                                    email_address=email_address,
                                    country=country)
    assert not isinstance(account, ServiceError)

    assert account["rec_id"] is not None
    assert account["account_id"] is not None
    assert account["username"] == username
    assert account["email_address"] == email_address
    assert account["country"] == country
    assert account["created_at"] is not None
    assert account["updated_at"] is not None

    # TODO: should we check the credentials were created correctly?
