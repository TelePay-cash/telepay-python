from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAsyncClient, TelePayAuth, TelePayError

from ..utils import random_text

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
async def test_get_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.get_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
async def test_cancel_invoice(client: TelePayAsyncClient, invoice: Invoice):
    await client.cancel_invoice(invoice.number)


@pytest_mark.anyio
async def test_cancel_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.cancel_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
async def test_delete_invoice(client: TelePayAsyncClient, invoice: Invoice):
    await client.cancel_invoice(invoice.number)
    await client.delete_invoice(invoice.number)


@pytest_mark.anyio
async def test_delete_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.delete_invoice(number)
        assert False
    except TelePayError as e:
        assert e.status_code == 404
        assert e.error == "not-found"
        assert e.message == f"Invoice with number {number} does not exist"


@pytest_mark.anyio
async def test_transfer_without_funds(client: TelePayAsyncClient):
    try:
        await client.transfer(
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
async def test_transfer_to_wrong_user(client: TelePayAsyncClient):
    username = random_text(20)
    try:
        await client.transfer(
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
async def test_transfer_to_itself(client: TelePayAsyncClient):
    account = await client.get_me()
    username = account.merchant["username"]
    try:
        await client.transfer(
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


@pytest_mark.anyio
async def test_get_withdraw_fee(client: TelePayAsyncClient):
    await client.get_withdraw_fee(
        to_address="EQCKYK7bYBt1t8UmdhImrbiSzC5ijfo_H3Zc_Hk8ksRpOkOk",
        asset="TON",
        blockchain="TON",
        network="testnet",
        amount=1,
        message="test",
    )


@pytest_mark.anyio
async def test_withdraw(client: TelePayAsyncClient):
    try:
        await client.withdraw(
            to_address="EQCKYK7bYBt1t8UmdhImrbiSzC5ijfo_H3Zc_Hk8ksRpOkOk",
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            message="test",
        )
    except TelePayError as e:
        assert e.status_code == 401
        assert e.error == "insufficient-funds"
        assert e.message == "Insufficient funds to withdraw"
