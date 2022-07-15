import logging
from dataclasses import dataclass, field
from typing import Union

from httpx._config import Timeout
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
from ..http_clients import SyncClient
from ..models.account import Account
from ..models.assets import Asset, Assets
from ..models.invoice import Invoice, InvoiceList
from ..models.wallets import Wallet, Wallets
from ..models.webhooks import Webhook, Webhooks
from ..utils import validate_response

logger = logging.getLogger(__name__)


@dataclass
class TelePaySyncClient:
    """
    Creates a TelePay client.
    * API_SECRET: Your merchant private API key.
    Any requests without this authentication key will result in error 403.
    """

    timeout: TimeoutTypes = field(default=Timeout(60))

    def __init__(self, secret_api_key, timeout=Timeout(60)) -> None:
        self.base_url = "https://api.telepay.cash/rest/"
        self.timeout = timeout
        self.http_client = SyncClient(
            base_url=self.base_url,
            headers={"Authorization": secret_api_key},
            timeout=self.timeout,
        )

    def __enter__(self) -> "TelePaySyncClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(auth: TelePayAuth, timeout=Timeout(60)) -> "TelePaySyncClient":
        return TelePaySyncClient(auth.secret_api_key, timeout=timeout)

    def get_me(self) -> Account:
        """
        Info about the current account
        """
        response = self.http_client.get("getMe")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Account.from_json(response.json())

    def get_balance(self, asset=None, blockchain=None, network=None) -> Union[Wallet, Wallets]:
        """
        Get your merchant wallet assets with corresponding balance
        """
        if asset and blockchain and network:
            response = self.http_client.post(
                "getBalance",
                json={"asset": asset, "blockchain": blockchain, "network": network},
            )
            logger.debug(f"response: {response.text}")

            validate_response(response)
            return Wallet.from_json(response.json())
        else:
            response = self.http_client.get("getBalance")
            logger.debug(f"response: {response.text}")

            validate_response(response)
            return Wallets.from_json(response.json())

    def get_asset(self, asset: str, blockchain: str) -> Asset:
        """
        Get asset details
        """
        response = self.http_client.request(
            method="GET",
            url="getAsset",
            json={
                "asset": asset,
                "blockchain": blockchain,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Asset.from_json(response.json())

    def get_assets(self) -> Assets:
        """
        Get assets suported by TelePay
        """
        response = self.http_client.get("getAssets")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Assets.from_json(response.json())

    def get_invoices(self) -> InvoiceList:
        """
        Get your merchant invoices
        """
        response = self.http_client.get("getInvoices")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return InvoiceList.from_json(response.json())

    def get_invoice(self, number: str) -> Invoice:
        """
        Get invoice details, by ID
        """
        response = self.http_client.get(f"getInvoice/{number}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Invoice.from_json(response.json())

    def create_invoice(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        success_url: str,
        cancel_url: str,
        expires_at: int,
        metadata: dict = None,
        description: str = None,
    ) -> Invoice:
        """
        Create an invoice
        """
        response = self.http_client.post(
            "createInvoice",
            json={
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
                "amount": amount,
                "description": description,
                "metadata": metadata,
                "success_url": success_url,
                "cancel_url": cancel_url,
                "expires_at": expires_at,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Invoice.from_json(response.json())

    def cancel_invoice(self, number: str) -> Invoice:
        """
        Cancel an invoice
        """
        response = self.http_client.post(f"cancelInvoice/{number}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Invoice.from_json(response.json())

    def delete_invoice(self, number: str) -> dict:
        """
        Delete an invoice
        """
        response = self.http_client.post(f"deleteInvoice/{number}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def transfer(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        username: str,
        message: str = None,
    ) -> dict:
        """
        Transfer funds between internal wallets.
        Off-chain operation.
        """
        response = self.http_client.post(
            "transfer",
            json={
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
                "amount": amount,
                "username": username,
                "message": message,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def get_withdraw_minimum(
        self,
        asset: str,
        blockchain: str,
        network: str = None,
    ) -> dict:
        """
        Get minimum withdraw amount.
        """
        response = self.http_client.post(
            "getWithdrawMinimum",
            json={
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def get_withdraw_fee(
        self,
        to_address: str,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        message: str = None,
    ) -> dict:
        """
        Get estimated withdraw fee, composed of blockchain fee and processing fee.
        """
        response = self.http_client.post(
            "getWithdrawFee",
            json={
                "to_address": to_address,
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
                "amount": amount,
                "message": message,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def withdraw(
        self,
        to_address: str,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        message: str,
    ) -> dict:
        """
        Withdraw funds from merchant wallet to external wallet.
        On-chain operation.
        """
        response = self.http_client.post(
            "withdraw",
            json={
                "to_address": to_address,
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
                "amount": amount,
                "message": message,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def create_webhook(
        self, url: str, secret: str, events: list, active: bool
    ) -> Webhook:
        """
        Create a webhook
        """
        response = self.http_client.post(
            "createWebhook",
            json={
                "url": url,
                "secret": secret,
                "events": events,
                "active": active,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhook.from_json(response.json())

    def update_webhook(
        self, id: str, url: str, secret: str, events: list, active: bool
    ) -> Webhook:
        """
        Update a webhook
        """
        response = self.http_client.post(
            f"updateWebhook/{id}",
            json={
                "url": url,
                "secret": secret,
                "events": events,
                "active": active,
            },
        )
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhook.from_json(response.json())

    def activate_webhook(self, id: str) -> Webhook:
        """
        Activate a webhook
        """
        response = self.http_client.post(f"activateWebhook/{id}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhook.from_json(response.json())

    def deactivate_webhook(self, id: str) -> Webhook:
        """
        Deactivate a webhook
        """
        response = self.http_client.post(f"deactivateWebhook/{id}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhook.from_json(response.json())

    def delete_webhook(self, id: str) -> dict:
        """
        Delete a webhook
        """
        response = self.http_client.post(f"deleteWebhook/{id}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return response.json()

    def get_webhook(self, id: str) -> Webhook:
        """
        Get webhook
        """
        response = self.http_client.get(f"getWebhook/{id}")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhook.from_json(response.json())

    def get_webhooks(self) -> Webhooks:
        """
        Get webhooks
        """
        response = self.http_client.get("getWebhooks")
        logger.debug(f"response: {response.text}")

        validate_response(response)
        return Webhooks.from_json(response.json())
