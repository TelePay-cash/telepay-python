from dataclasses import dataclass, field
from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
from ..errors import TelePayError
from ..http_clients import SyncClient
from ..utils import validate_response

from ..models.info import Info
from ..models.invoice import Invoice
from ..models.transfer import Transfer
from ..models.withdraw import Withdraw
from ..models.balance import Balance
from ..models.assets import Assets


@dataclass
class SyncTelePayClient:
    """
    Creates a TelePay client.
    * API_SECRET: Your merchant private API key.
    Any requests without this authentication key will result in error 403.
    """

    api_secret: str
    timeout: TimeoutTypes = field(default=DEFAULT_TIMEOUT_CONFIG)

    def __post_init__(self):
        self.auth_params = {'api_secret': self.api_secret}
        self.base_url = 'https://api.telepay.cash/rest/'
        self.http_client = SyncClient(
            base_url=self.base_url,
            params=self.auth_params,
            timeout=self.timeout,
        )

    def __enter__(self) -> 'SyncTelePayClient':
        return self

    def __exit__(self) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: TelePayAuth,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    ) -> "SyncTelePayClient":
        return SyncTelePayClient(auth.api_secret, timeout)

    def getMe(
        self,
        name: str,
        url: str,
        logo_url: str,
        logo_thumbnail_url: str,
        first_name: str,
        last_name: str,
        username: str,
    ) -> Info:
        """
        Info about the current merchant.
        """

        response = self.http_client.get('getMe', json={
            'name': name,
            'url': url,
            'logo_url': logo_url,
            'logo_thumbnail_url': logo_thumbnail_url,
            'first_name': first_name,
            'last_name': last_name,
            'username': username
        })
        validate_response(response)
        return Info.from_json(response.json())

    def getBalance(
        self,
        asset: str,
        blockchain: str,
        balance: float,
    ) -> Balance:
        """
        Get your merchant wallet assets with corresponding balance
        """

        response = self.http_client.get('getBalance', json={
            'asset': asset,
            'blockchain': blockchain,
            'balance': balance,
        })
        validate_response(response)
        return Balance.from_json(response.json())

    def getAssets(
            self,
            assets: str,
            blockchain: str) -> Assets:
        """
        Get assets suported by TelePay
        """

        response = self.http_client.get('getAssets', json={
            'assets': assets,
            'blockchain': blockchain
        })
        validate_response(response)
        return Assets.from_json(response.json())

    def getInvoices(self) -> Invoice:
        """
        Get your merchant invoices
        """

        response = self.http_client.get('getInvoices')
        validate_response(response)
        return response.json()

    def getInvoice(self) -> Invoice:
        """
        Get invoice details, by ID
        """
        response = self.http_client.get('getInvoice/{invoice_id}')
        validate_response(response)
        return response.json()

    def createInvoice(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        description: str,
        success_url: str,
        cancel_url: str,
        expires_at: int
    ) -> Invoice:
        """
        Create an invoice
        """

        response = self.http_client.post('createInvoice', json={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'description': description,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'expires_at': expires_at
        })
        validate_response(response)
        return Invoice.from_json(response.json())

    def transfer(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        username: str,
        message: str
    ) -> Transfer:
        """
        Transfer funds between internal wallets.
        Off-chain operation.
        """

        response = self.http_client.post('transfer', json={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'username': username,
            'message': message
        })
        validate_response(response)
        return Transfer.from_json(response.json())

    def withdraw(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str
    ) -> Withdraw:
        """
        Withdraw funds from merchant wallet to external wallet.
        On-chain operation.
        """
        response = self.http_client.post('withdraw', json={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'to_address': to_address,
            'message': message}
        )
        validate_response(response)
        return Withdraw.from_json(response.json())

    def getWithdrawFee(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str
    ) -> Withdraw:
        """
        Get estimated withdraw fee, composed of blockchain fee and processing fee.
        """
        response = self.http_client.post('getWithdrawFee', json={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'to_address': to_address,
            'message': message}
        )
        validate_response(response)
        return Withdraw.from_json(response.json())
