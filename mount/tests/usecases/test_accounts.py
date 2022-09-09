import pytest
from app.common.context import Context
from app.usecases import accounts

# https://docs.pytest.org/en/7.1.x/reference/reference.html#globalvar-pytestmark
pytestmark = pytest.mark.asyncio


async def test_should_pass(ctx: Context):
    assert True
