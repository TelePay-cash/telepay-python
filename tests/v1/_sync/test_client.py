import os

from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from telepay.v1 import Invoice, TelePayAuth, TelePayError, TelePaySyncClient, Webhook

from ..utils import ERRORS, random_text

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


@fixture(name="webhook")
def create_webhook(client: TelePaySyncClient):
    webhook = client.create_webhook(
        url="https://example.com", secret="hello", events=["all"], active=False
    )
    yield webhook


@pytest_mark.anyio
def test_error(client: TelePaySyncClient):
    client = TelePaySyncClient("")
    try:
        client.get_me()
        assert False
    except TelePayError:
        assert True


@pytest_mark.anyio
def test_client_with_context():
    api_key = os.environ["TELEPAY_SECRET_API_KEY"]
    # TODO: add more tests and ensure the client api is the same
    with TelePaySyncClient(secret_api_key=api_key) as client:
        assert client is not None


@pytest_mark.anyio
def test_get_me(client: TelePaySyncClient):
    try:
        client.get_me()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_balance(client: TelePaySyncClient):
    try:
        client.get_balance()
        client.get_balance(asset="TON", blockchain="TON", network="testnet")
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_asset(client: TelePaySyncClient):
    try:
        client.get_asset(asset="TON", blockchain="TON")
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_assets(client: TelePaySyncClient):
    try:
        client.get_assets()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_invoices(client: TelePaySyncClient):
    try:
        client.get_invoices()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_invoice(client: TelePaySyncClient, invoice: Invoice):
    try:
        client.get_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.get_invoice(number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
def test_cancel_invoice(client: TelePaySyncClient, invoice: Invoice):
    try:
        client.cancel_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
def test_cancel_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.cancel_invoice(number)
        assert False
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
def test_delete_invoice(client: TelePaySyncClient, invoice: Invoice):
    try:
        client.cancel_invoice(invoice.number)
        client.delete_invoice(invoice.number)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


@pytest_mark.anyio
def test_delete_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    try:
        client.delete_invoice(number)
        assert False
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        elif e.status_code == 404:
            assert e.error == "invoice.not-found"
            assert e.message == ERRORS["invoice.not-found"]


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
        if e.status_code == 401:
            assert e.error == "transfer.not-possible"
            assert e.message == ERRORS["transfer.not-possible"]
        elif e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_withdraw_minimum(client: TelePaySyncClient):
    try:
        client.get_withdraw_minimum(
            asset="TON",
            blockchain="TON",
            network="testnet",
        )
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]


@pytest_mark.anyio
def test_get_withdraw_fee(client: TelePaySyncClient):
    try:
        client.get_withdraw_fee(
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
def test_withdraw(client: TelePaySyncClient):
    try:
        client.withdraw(
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
def test_update_webhook(client: TelePaySyncClient, webhook: Webhook):
    try:
        client.update_webhook(
            id=webhook.id,
            url="https://example.com",
            secret="hello",
            events=["invoice.completed"],
            active=False,
        )
        client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
def test_activate_webhook(client: TelePaySyncClient, webhook: Webhook):
    try:
        client.activate_webhook(id=webhook.id)
        client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
def test_deactivate_webhook(client: TelePaySyncClient, webhook: Webhook):
    try:
        client.deactivate_webhook(id=webhook.id)
        client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
def test_delete_webhook(client: TelePaySyncClient, webhook: Webhook):
    try:
        client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
def test_get_webhook(client: TelePaySyncClient, webhook: Webhook):
    try:
        client.get_webhook(id=webhook.id)
        client.delete_webhook(id=webhook.id)
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]


@pytest_mark.anyio
def test_get_webhooks(client: TelePaySyncClient):
    try:
        client.get_webhooks()
    except TelePayError as e:
        if e.status_code == 403:
            assert e.error == "forbidden"
            assert e.message == ERRORS["forbidden"]
        if e.status_code == 404:
            assert e.error == "webhook.not-found"
            assert e.message == ERRORS["webhook.not-found"]
