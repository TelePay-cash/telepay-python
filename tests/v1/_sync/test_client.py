from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAuth, TelePayError, TelePaySyncClient

TIMEOUT = 20


@fixture(name="client")
def create_client():
    client = TelePaySyncClient.from_auth(TelePayAuth(), timeout=Timeout(TIMEOUT))
    yield client
    client.close()


@fixture(name="invoice")
def create_invoice(client: TelePaySyncClient):
    invoice = client.create_invoice(
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
def test_error(client: TelePaySyncClient):
    client = TelePaySyncClient("")
    try:
        client.get_me()
        assert False
    except TelePayError:
        assert True


@pytest_mark.anyio
def test_get_me(client: TelePaySyncClient):
    client.get_me()


@pytest_mark.anyio
def test_get_balance(client: TelePaySyncClient):
    client.get_balance()


@pytest_mark.anyio
def test_get_assets(client: TelePaySyncClient):
    client.get_assets()


@pytest_mark.anyio
def test_get_invoices(client: TelePaySyncClient):
    client.get_invoices()


@pytest_mark.anyio
def test_get_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.get_invoice(invoice.number)


@pytest_mark.anyio
def test_cancel_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.cancel_invoice(invoice.number)


@pytest_mark.anyio
def test_delete_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.cancel_invoice(invoice.number)
    client.delete_invoice(invoice.number)
