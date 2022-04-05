from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAsyncClient, TelePayAuth, TelePayError

TIMEOUT = 20


@fixture(name="client")
async def create_client():
    client = TelePayAsyncClient.from_auth(TelePayAuth(), timeout=Timeout(TIMEOUT))
    yield client
    await client.close()


@fixture(name="invoice")
async def create_invoice(client: TelePayAsyncClient):
    invoice = await client.create_invoice(
        asset="TON",
        blockchain="TON",
        network="testnet",
        amount=1,
        description="Testing",
        metadata={"color": "red", "size": "large"},
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        expires_at=1,
    )
    yield invoice


@pytest_mark.anyio
async def test_error(client: TelePayAsyncClient):
    client = TelePayAsyncClient("")
    try:
        await client.get_me()
        assert False
    except TelePayError:
        assert True


@pytest_mark.anyio
async def test_get_me(client: TelePayAsyncClient):
    await client.get_me()


@pytest_mark.anyio
async def test_get_balance(client: TelePayAsyncClient):
    await client.get_balance()


@pytest_mark.anyio
async def test_get_assets(client: TelePayAsyncClient):
    await client.get_assets()


@pytest_mark.anyio
async def test_get_invoices(client: TelePayAsyncClient):
    await client.get_invoices()


@pytest_mark.anyio
async def test_get_invoice(client: TelePayAsyncClient, invoice: Invoice):
    await client.get_invoice(invoice.number)


@pytest_mark.anyio
async def test_cancel_invoice(client: TelePayAsyncClient, invoice: Invoice):
    await client.cancel_invoice(invoice.number)


@pytest_mark.anyio
async def test_delete_invoice(client: TelePayAsyncClient, invoice: Invoice):
    await client.cancel_invoice(invoice.number)
    await client.delete_invoice(invoice.number)
