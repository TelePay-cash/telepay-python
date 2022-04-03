from dataclasses import dataclass, field
from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
from ..http_clients import AsyncClient
from ..utils import validate_response

from ..models.account import Account
from ..models.invoice import Invoice, InvoiceList

# from ..models.transfer import Transfer
# from ..models.withdraw import Withdraw
from ..models.wallets import Wallets
from ..models.assets import Assets


@dataclass
class TelePayAsyncClient:
    """
    Creates a TelePay async client.
    * API_SECRET: Your merchant private API key.
    Any requests without this authentication key will result in error 403.
    """

    timeout: TimeoutTypes = field(default=DEFAULT_TIMEOUT_CONFIG)

    def __init__(self, secret_api_key) -> None:
        self.base_url = "https://api.telepay.cash/rest/"
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
    def from_auth(auth: TelePayAuth) -> "TelePayAsyncClient":
        return TelePayAsyncClient(auth.secret_api_key)

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
