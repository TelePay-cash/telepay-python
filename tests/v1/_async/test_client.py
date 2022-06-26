import os
import uuid

from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAsyncClient, TelePayAuth, TelePayError, Webhook

from ..utils import ERRORS, random_text

TIMEOUT = 60


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


@fixture(name="webhook")
async def create_webhook(client: TelePayAsyncClient):
    webhook = await client.create_webhook(
        url=f"https://{uuid.uuid4().hex}.com", secret="hello", events=["all"], active=False
    )
    yield webhook


@pytest_mark.anyio
async def test_error(client: TelePayAsyncClient):
    client = TelePayAsyncClient("")
    try:
        await client.get_me()
        assert False
    except TelePayError:
        assert True


@pytest_mark.anyio
async def test_client_with_context():
    api_key = os.environ["TELEPAY_SECRET_API_KEY"]
    # TODO: add more tests and ensure the client api is the same
    async with TelePayAsyncClient(secret_api_key=api_key) as client:
        assert client is not None


@pytest_mark.anyio
async def test_get_me(client: TelePayAsyncClient):
    try:
        await client.get_me()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_balance(client: TelePayAsyncClient):
    try:
        await client.get_balance()
        await client.get_balance(asset="TON", blockchain="TON", network="testnet")
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_asset(client: TelePayAsyncClient):
    try:
        await client.get_asset(asset="TON", blockchain="TON")
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_assets(client: TelePayAsyncClient):
    try:
        await client.get_asset(asset="TON", blockchain="TON")
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_invoices(client: TelePayAsyncClient):
    try:
        await client.get_invoices()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_invoice(client: TelePayAsyncClient, invoice: Invoice):
    try:
        await client.get_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.get_invoice(number)
        assert False
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
async def test_cancel_invoice(client: TelePayAsyncClient, invoice: Invoice):
    try:
        await client.cancel_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
async def test_cancel_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.cancel_invoice(number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
async def test_delete_invoice(client: TelePayAsyncClient, invoice: Invoice):
    try:
        await client.cancel_invoice(invoice.number)
        await client.delete_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
async def test_delete_invoice_not_found(client: TelePayAsyncClient):
    number = random_text(10)
    try:
        await client.delete_invoice(number)
        assert False
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


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
        if e.status_code == 401:
            assert e.error == "transfer.insufficient-funds"
            assert e.message == ERRORS["transfer.insufficient-funds"]
        elif e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


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
        if e.status_code == 401:
            assert e.error == "transfer.insufficient-funds"
            assert e.message == ERRORS["transfer.insufficient-funds"]
        elif e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "account.not-found"
            assert e.message == ERRORS["account.not-found"]


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
        if e.status_code == 401:
            assert e.error == "transfer.not-possible"
            assert e.message == ERRORS["transfer.not-possible"]
        elif e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_withdraw_minimum(client: TelePayAsyncClient):
    try:
        await client.get_withdraw_minimum(
            asset="TON",
            blockchain="TON",
            network="testnet",
        )
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_get_withdraw_fee(client: TelePayAsyncClient):
    try:
        await client.get_withdraw_fee(
            to_address="EQCKYK7bYBt1t8UmdhImrbiSzC5ijfo_H3Zc_Hk8ksRpOkOk",
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            message="test",
        )
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


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
        if e.status_code == 503:
            assert e.error == "unavailable"
            assert e.message == ERRORS["unavailable"]
        elif e.status_code == 401:
            assert e.error == "withdrawal.insufficient-funds"
            assert e.message == ERRORS["withdrawal.insufficient-funds"]
        elif e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
async def test_update_webhook(client: TelePayAsyncClient, webhook: Webhook):
    try:
        await client.update_webhook(
            id=webhook.id,
            url="https://example.com",
            secret="hello",
            events=["invoice.completed"],
            active=False,
        )
        await client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
async def test_activate_webhook(client: TelePayAsyncClient, webhook: Webhook):
    try:
        await client.activate_webhook(id=webhook.id)
        await client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
async def test_deactivate_webhook(client: TelePayAsyncClient, webhook: Webhook):
    try:
        await client.deactivate_webhook(id=webhook.id)
        await client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
async def test_delete_webhook(client: TelePayAsyncClient, webhook: Webhook):
    try:
        await client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
async def test_get_webhook(client: TelePayAsyncClient, webhook: Webhook):
    try:
        await client.get_webhook(id=webhook.id)
        await client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
async def test_get_webhooks(client: TelePayAsyncClient):
    try:
        await client.get_webhooks()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]
