import logging
from dataclasses import dataclass, field
from typing import Union

from httpx._config import Timeout
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
from ..http_clients import AsyncClient
from ..models.account import Account
from ..models.assets import Asset, Assets
from ..models.invoice import Invoice, InvoiceList
from ..models.wallets import Wallet, Wallets
from ..models.webhooks import Webhook, Webhooks
from ..utils import validate_response

logger = logging.getLogger(__name__)


@dataclass
class TelePayAsyncClient:
    """
    Creates a TelePay async client.
    * API_SECRET: Your merchant private API key.
    Any requests without this authentication key will result in error 403.
    """

    timeout: TimeoutTypes = field(default=Timeout(60))

    def __init__(self, secret_api_key, timeout=Timeout(60)) -> None:
        self.base_url = "https://api.telepay.cash/rest/"
        self.timeout = timeout
        self.http_client = AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": secret_api_key},
            timeout=self.timeout,
        )

    async def __aenter__(self) -> "TelePayAsyncClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.http_client.aclose()

    @staticmethod
    def from_auth(auth: TelePayAuth, timeout=Timeout(60)) -> "TelePayAsyncClient":
        return TelePayAsyncClient(auth.secret_api_key, timeout=timeout)

    async def get_me(self) -> Account:
        """
        Info about the current account
        """
        response = await self.http_client.get("getMe")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Account.from_json(response.json())

    async def get_balance(
        self, asset=None, blockchain=None, network=None
    ) -> Union[Wallet, Wallets]:
        """
        Get your merchant wallet assets with corresponding balance
        """
        if asset and blockchain and network:
            response = await self.http_client.post(
                "getBalance",
                json={"asset": asset, "blockchain": blockchain, "network": network},
            )
            logger.debug(f"Response: {response.text}")
            validate_response(response)
            return Wallets.from_json(response.json())
        else:
            response = await self.http_client.get("getBalance")
            logger.debug(f"Response: {response.text}")
            validate_response(response)
            return Wallets.from_json(response.json())

    async def get_asset(self, asset: str, blockchain: str) -> Asset:
        """
        Get asset details
        """
        response = await self.http_client.request(
            method="GET",
            url="getAsset",
            json={
                "asset": asset,
                "blockchain": blockchain,
            },
        )
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Asset.from_json(response.json())

    async def get_assets(self) -> Assets:
        """
        Get assets suported by TelePay
        """
        response = await self.http_client.get("getAssets")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Assets.from_json(response.json())

    async def get_invoices(self) -> InvoiceList:
        """
        Get your merchant invoices
        """
        response = await self.http_client.get("getInvoices")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return InvoiceList.from_json(response.json())

    async def get_invoice(self, number: str) -> Invoice:
        """
        Get invoice details, by ID
        """
        response = await self.http_client.get(f"getInvoice/{number}")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Invoice.from_json(response.json())

    async def create_invoice(
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
        response = await self.http_client.post(
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
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Invoice.from_json(response.json())

    async def cancel_invoice(self, number: str) -> Invoice:
        """
        Cancel an invoice
        """
        response = await self.http_client.post(f"cancelInvoice/{number}")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Invoice.from_json(response.json())

    async def delete_invoice(self, number: str) -> dict:
        """
        Delete an invoice
        """
        response = await self.http_client.post(f"deleteInvoice/{number}")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def transfer(
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
        response = await self.http_client.post(
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
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def get_withdraw_minimum(
        self,
        asset: str,
        blockchain: str,
        network: str = None,
    ) -> dict:
        """
        Get minimum withdraw amount.
        """
        response = await self.http_client.post(
            "getWithdrawMinimum",
            json={
                "asset": asset,
                "blockchain": blockchain,
                "network": network,
            },
        )
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def get_withdraw_fee(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str = None,
    ) -> dict:
        """
        Get estimated withdraw fee, composed of blockchain fee and processing fee.
        """
        response = await self.http_client.post(
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
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def withdraw(
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
        response = await self.http_client.post(
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
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def create_webhook(
        self, url: str, secret: str, events: list, active: bool
    ) -> Webhook:
        """
        Create a webhook
        """
        response = await self.http_client.post(
            "createWebhook",
            json={
                "url": url,
                "secret": secret,
                "events": events,
                "active": active,
            },
        )
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Webhook.from_json(response.json())

    async def update_webhook(
        self, id: str, url: str, secret: str, events: list, active: bool
    ) -> Webhook:
        """
        Update a webhook
        """
        response = await self.http_client.post(
            f"updateWebhook/{id}",
            json={
                "url": url,
                "secret": secret,
                "events": events,
                "active": active,
            },
        )
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Webhook.from_json(response.json())

    async def activate_webhook(self, id: str) -> Webhook:
        """
        Activate a webhook
        """
        response = await self.http_client.post(f"activateWebhook/{id}")
        validate_response(response)
        return Webhook.from_json(response.json())

    async def deactivate_webhook(self, id: str) -> Webhook:
        """
        Deactivate a webhook
        """
        response = await self.http_client.post(f"deactivateWebhook/{id}")
        validate_response(response)
        return Webhook.from_json(response.json())

    async def delete_webhook(self, id: str) -> dict:
        """
        Delete a webhook
        """
        response = await self.http_client.post(f"deleteWebhook/{id}")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return response.json()

    async def get_webhook(self, id: str) -> Webhook:
        """
        Get webhook
        """
        response = await self.http_client.get(f"getWebhook/{id}")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Webhook.from_json(response.json())

    async def get_webhooks(self) -> Webhooks:
        """
        Get webhooks
        """
        response = await self.http_client.get("getWebhooks")
        logger.debug(f"Response: {response.text}")
        validate_response(response)
        return Webhooks.from_json(response.json())
