import os
import uuid

import pytest
from httpx import Timeout

from telepay.v1 import Invoice, TelePayAuth, TelePayError, TelePaySyncClient, Webhook

from ..utils import ERRORS, random_text

TIMEOUT = 60


@pytest.fixture(name="client")
def create_client():
    client = TelePaySyncClient.from_auth(TelePayAuth(), timeout=Timeout(TIMEOUT))
    yield client
    client.close()


@pytest.fixture(name="invoice")
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


@pytest.fixture(name="webhook")
def create_webhook(client: TelePaySyncClient):
    webhook = client.create_webhook(
        url=f"https://{uuid.uuid4().hex}.com",
        secret="hello",
        events=["all"],
        active=False,
    )
    yield webhook


def test_error(client: TelePaySyncClient):
    client = TelePaySyncClient("")
    with pytest.raises(TelePayError):
        client.get_me()


def test_client_with_context():
    api_key = os.environ["TELEPAY_SECRET_API_KEY"]
    # TODO: add more tests and ensure the client api is the same
    with TelePaySyncClient(secret_api_key=api_key) as client:
        assert client is not None


def test_get_me(client: TelePaySyncClient):
    account = client.get_me()
    assert account is not None


def test_get_balance(client: TelePaySyncClient):
    balance = client.get_balance()
    assert len(balance.wallets) == 4  # TON, TON_testnet, Hive, HBD

    ton_balance = client.get_balance(asset="TON", blockchain="TON", network="testnet")
    assert ton_balance.asset == "TON"
    assert ton_balance.blockchain == "TON"
    assert ton_balance.network == "testnet"
    assert ton_balance.balance == 0


def test_get_asset(client: TelePaySyncClient):
    asset = client.get_asset(asset="TON", blockchain="TON")
    assert asset.asset == "TON"
    assert asset.blockchain == "TON"
    assert asset.networks == ["mainnet", "testnet"]
    assert asset.coingecko_id == "the-open-network"
    assert asset.url == "https://ton.org"
    assert asset.usd_price is not None


def test_get_assets(client: TelePaySyncClient):
    assets = client.get_assets()
    assert len(assets.assets) == 3  # TON, Hive, HBD


def test_get_invoices(client: TelePaySyncClient):
    invoices = client.get_invoices()
    assert len(invoices.invoices) > 0
    assert invoices.invoices[0].checkout_url is not None


def test_get_invoice(client: TelePaySyncClient, invoice: Invoice):
    invoice = client.get_invoice(invoice.number)
    assert invoice.asset == "TON"
    assert invoice.blockchain == "TON"
    assert invoice.network == "testnet"
    assert float(invoice.amount) == 1.0
    assert invoice.description == "Testing"
    assert invoice.success_url == "https://example.com/success"
    assert invoice.cancel_url == "https://example.com/cancel"


def test_get_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    with pytest.raises(TelePayError) as error:
        client.get_invoice(number)

    assert error.value.status_code == 404
    assert error.value.error == "invoice.not-found"
    assert error.value.message == ERRORS["invoice.not-found"]


def test_cancel_invoice(client: TelePaySyncClient, invoice: Invoice):
    invoice = client.cancel_invoice(invoice.number)
    assert invoice.status == "cancelled"
    assert invoice.asset == "TON"
    assert invoice.blockchain == "TON"
    assert invoice.network == "testnet"
    assert float(invoice.amount) == 1.0
    assert invoice.description == "Testing"


def test_cancel_invoice_already_canceled(client: TelePaySyncClient):
    with pytest.raises(TelePayError) as error:
        client.cancel_invoice("SORR79EBLB")
    print(error.value)

    assert error.value.status_code == 304
    assert error.value.error == 304
    assert error.value.message == b""


def test_cancel_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    with pytest.raises(TelePayError) as error:
        client.cancel_invoice(number)

    assert error.value.status_code == 404
    assert error.value.error == "invoice.not-found"
    assert error.value.message == ERRORS["invoice.not-found"]


def test_delete_invoice(client: TelePaySyncClient, invoice: Invoice):
    client.cancel_invoice(invoice.number)
    response = client.delete_invoice(invoice.number)
    assert response.get("success") == "invoice.deleted"
    assert response.get("message") == "Invoice deleted."


def test_delete_invoice_not_found(client: TelePaySyncClient):
    number = random_text(10)
    with pytest.raises(TelePayError) as error:
        client.delete_invoice(number)

    assert error.value.status_code == 404
    assert error.value.error == "invoice.not-found"
    assert error.value.message == ERRORS["invoice.not-found"]


def test_transfer_without_funds(client: TelePaySyncClient):
    with pytest.raises(TelePayError) as error:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username="telepay",
        )

    assert error.value.status_code == 401
    assert error.value.error == "transfer.insufficient-funds"
    assert error.value.message == ERRORS["transfer.insufficient-funds"]


def test_transfer_to_wrong_user(client: TelePaySyncClient):
    username = random_text(20)
    with pytest.raises(TelePayError) as error:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username=username,
        )

    assert error.value.status_code == 404
    assert error.value.error == "account.not-found"
    assert error.value.message == ERRORS["account.not-found"]


def test_transfer_to_itself(client: TelePaySyncClient):
    username = client.get_me().merchant["username"]
    with pytest.raises(TelePayError) as error:
        client.transfer(
            asset="TON",
            blockchain="TON",
            network="testnet",
            amount=1,
            username=username,
        )

    assert error.value.status_code == 401
    assert error.value.error == "transfer.not-possible"
    assert error.value.message == ERRORS["transfer.not-possible"]


def test_withdraw_minimum(client: TelePaySyncClient):
    response = client.get_withdraw_minimum(
        asset="TON",
        blockchain="TON",
        network="testnet",
    )

    assert response.get("withdraw_minimum") == 0.2


def test_get_withdraw_fee(client: TelePaySyncClient):
    response = client.get_withdraw_fee(
        to_address="EQCKYK7bYBt1t8UmdhImrbiSzC5ijfo_H3Zc_Hk8ksRpOkOk",
        asset="TON",
        blockchain="TON",
        network="testnet",
        amount=1,
        message="test",
    )
    assert response.get("blockchain_fee") > 0
    assert response.get("processing_fee") > 0
    assert response.get("total") > 0


@pytest.mark.skip(reason="Withdraw is disabled")
def test_withdraw(client: TelePaySyncClient):
    response = client.withdraw(
        to_address="EQCKYK7bYBt1t8UmdhImrbiSzC5ijfo_H3Zc_Hk8ksRpOkOk",
        asset="TON",
        blockchain="TON",
        network="testnet",
        amount=1,
        message="test",
    )
    print(response)


def test_update_webhook(client: TelePaySyncClient, webhook: Webhook):
    webhook_updated = client.update_webhook(
        id=webhook.id,
        url="https://example.com",
        secret="hello",
        events=["invoice.completed"],
        active=False,
    )
    assert webhook_updated.id == webhook.id
    assert webhook_updated.url == "https://example.com"
    assert webhook_updated.secret == "hello"
    # assert webhook_updated.events == ["invoice.completed"]  # always returns ['all']
    assert webhook_updated.active is False

    client.delete_webhook(id=webhook.id)


def test_activate_webhook(client: TelePaySyncClient, webhook: Webhook):
    webhook_updated = client.activate_webhook(id=webhook.id)
    assert webhook_updated.active is True
    assert webhook_updated.id == webhook.id

    client.delete_webhook(id=webhook.id)


def test_deactivate_webhook(client: TelePaySyncClient, webhook: Webhook):
    webhook_updated = client.deactivate_webhook(id=webhook.id)
    assert webhook_updated.active is False
    assert webhook_updated.id == webhook.id

    client.delete_webhook(id=webhook.id)


def test_delete_webhook(client: TelePaySyncClient, webhook: Webhook):
    response = client.delete_webhook(id=webhook.id)
    assert response.get("success") == "webhook.deleted"
    assert response.get("message") == "Webhook deleted."


def test_get_webhook(client: TelePaySyncClient, webhook: Webhook):
    webhook_updated = client.get_webhook(id=webhook.id)
    assert webhook_updated.id == webhook.id
    assert webhook_updated.url == webhook.url
    assert webhook_updated.secret == webhook.secret
    assert webhook_updated.events == webhook.events
    assert webhook_updated.active is webhook.active

    client.delete_webhook(id=webhook.id)


def test_get_webhooks(client: TelePaySyncClient):
    webhooks = client.get_webhooks()
    assert len(webhooks.webhooks) > 0
    assert webhooks.webhooks[0].id is not None
    assert webhooks.webhooks[0].url is not None
    assert webhooks.webhooks[0].secret is not None
