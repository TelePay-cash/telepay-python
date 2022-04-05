from dataclasses import dataclass, field

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
from ..http_clients import AsyncClient
from ..models.account import Account
from ..models.assets import Assets
from ..models.invoice import Invoice, InvoiceList
from ..models.wallets import Wallets
from ..models.withdraw import Withdraw
from ..utils import validate_response


@dataclass
class TelePayAsyncClient:
    """
    Creates a TelePay async client.
    * API_SECRET: Your merchant private API key.
    Any requests without this authentication key will result in error 403.
    """

    timeout: TimeoutTypes = field(default=DEFAULT_TIMEOUT_CONFIG)

    def __init__(self, secret_api_key, timeout=DEFAULT_TIMEOUT_CONFIG) -> None:
        self.base_url = "https://api.telepay.cash/rest/"
        self.timeout = timeout
        self.http_client = AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": secret_api_key},
            timeout=self.timeout,
        )

    async def __aenter__(self) -> "TelePayAsyncClient":
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: TelePayAuth, timeout=DEFAULT_TIMEOUT_CONFIG
    ) -> "TelePayAsyncClient":
        return TelePayAsyncClient(auth.secret_api_key, timeout=timeout)

    async def get_me(self) -> Account:
        """
        Info about the current account
        """
        response = await self.http_client.get("getMe")
        validate_response(response)
        return Account.from_json(response.json())

    async def get_balance(self) -> Wallets:
        """
        Get your merchant wallet assets with corresponding balance
        """
        response = await self.http_client.get("getBalance")
        validate_response(response)
        return Wallets.from_json(response.json())

    async def get_assets(self) -> Assets:
        """
        Get assets suported by TelePay
        """
        response = await self.http_client.get("getAssets")
        validate_response(response)
        return Assets.from_json(response.json())

    async def get_invoices(self) -> InvoiceList:
        """
        Get your merchant invoices
        """
        response = await self.http_client.get("getInvoices")
        validate_response(response)
        return InvoiceList.from_json(response.json())

    async def get_invoice(self, number: str) -> Invoice:
        """
        Get invoice details, by ID
        """
        response = await self.http_client.get(f"getInvoice/{number}")
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
        validate_response(response)
        return Invoice.from_json(response.json())

    async def cancel_invoice(self, number: str) -> Invoice:
        """
        Cancel an invoice
        """
        response = await self.http_client.post(f"cancelInvoice/{number}")
        validate_response(response)
        return Invoice.from_json(response.json())

    async def delete_invoice(self, number: str) -> dict:
        """
        Delete an invoice
        """
        response = await self.http_client.post(f"deleteInvoice/{number}")
        validate_response(response)
        return response.json()

    async def transfer(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        username: str,
        message: str,
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
        validate_response(response)
        return response.json()

    async def withdraw(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str,
    ) -> Withdraw:
        """
        Withdraw funds from merchant wallet to external wallet.
        On-chain operation.
        """
        # response = await self.http_client.post(
        #     "withdraw",
        #     json={
        #         "asset": asset,
        #         "blockchain": blockchain,
        #         "network": network,
        #         "amount": amount,
        #         "to_address": to_address,
        #         "message": message,
        #     },
        # )
        # validate_response(response)
        # return Withdraw.from_json(response.json())
        raise NotImplementedError()

    async def getWithdrawFee(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str,
    ) -> Withdraw:
        """
        Get estimated withdraw fee, composed of blockchain fee and processing fee.
        """
        # response = await self.http_client.post(
        #     "getWithdrawFee",
        #     json={
        #         "asset": asset,
        #         "blockchain": blockchain,
        #         "network": network,
        #         "amount": amount,
        #         "to_address": to_address,
        #         "message": message,
        #     },
        # )
        # validate_response(response)
        # return Withdraw.from_json(response.json())
        raise NotImplementedError()
