from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAuth, TelePayError, TelePaySyncClient

from ..utils import random_text

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
def test_get_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.get_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
def test_cancel_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.cancel_invoice(invoice.number)


@pytest_mark.anyio
def test_cancel_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.cancel_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
def test_delete_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.cancel_invoice(invoice.number)
    client.delete_invoice(invoice.number)


@pytest_mark.anyio
def test_delete_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.delete_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
def test_transfer_without_funds(client: TelePaySyncClient):
    try:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username="telepay",
        )
    except TelePayError as e:
        assert e.status_code == 401
        assert e.error == "insufficient-funds"
        assert e.message == "Insufficient funds to transfer"


@pytest_mark.anyio
def test_transfer_to_wrong_user(client: TelePaySyncClient):
    username = random_text(20)
    try:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username=username,
        )
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"User or merchant with username {username} does not exist"


@pytest_mark.anyio
def test_transfer_to_itself(client: TelePaySyncClient):
    username = client.get_me().merchant["username"]
    try:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username=username,
        )
    except TelePayError as e:
        assert e.status_code == 401
        assert e.error == "not-possible"
        assert e.message == "Can not transfer funds from the same wallet to itself"
