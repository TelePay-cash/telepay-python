from dataclasses import dataclass, field
from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..auth import TelePayAuth
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

        response = self.http_client.get('getMe', params={
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

        response = self.http_client.get('getBalance', params={
            'asset': asset,
            'blockchain': blockchain,
            'balance': balance,
        })
        validate_response(response)
        return Balance.from_json(response.json())

    def getAssets(
        self,
        assets: str,
        blockchain: str,
        url: str,
        networks: str
    ) -> Assets:
        """
        Get assets suported by TelePay
        """

        response = self.http_client.get('getAssets', params={
            'url': url,
            'assets': assets,
            'blockchain': blockchain,
            'networks': networks,
        })
        validate_response(response)
        return Assets.from_json(response.json())

    def getInvoices(
        self,
        asset: str,
        blockchain: str,
        amount: str,
        status: str,
        number: str,
        description: str,
        metadata: str,
        hidden_message: str,
        created_at: str,
        updated_at: str,
    ) -> Invoice:
        """
        Get your merchant invoices
        """
        response = self.http_client.get(f'getInvoices', params={
            'number': number,
            'asset': asset,
            'blockchain': blockchain,
            'status': status,
            'amount': amount,
            'description': description,
            'hidden_message': hidden_message,
            'metadata': metadata,
            'created_at': created_at,
            'updated_at': updated_at,
        })
        validate_response(response)
        return Invoice.from_json(response.json())

    def getInvoice(
        self,
        asset: str,
        blockchain: str,
        amount: str,
        status: str,
        number: str,
        description: str,
        metadata: str,
        hidden_message: str,
        created_at: str,
        updated_at: str,
    ) -> Invoice:
        """
        Get invoice details, by ID
        """
        response = self.http_client.get(f'getInvoice/{number}', params={
            'number': number,
            'asset': asset,
            'blockchain': blockchain,
            'status': status,
            'amount': amount,
            'description': description,
            'hidden_message': hidden_message,
            'metadata': metadata,
            'created_at': created_at,
            'updated_at': updated_at,
        })
        validate_response(response)
        return Invoice.from_json(response.json())

    def createInvoice(
        self,
        number: str,
        asset: str,
        blockchain: str,
        network: str,
        status: str,
        amount: float,
        description: str,
        hidden_message: str,
        success_url: str,
        cancel_url: str,
        explorer_url: str,
        checkout_url: str,
        expires_at: int,
        created_at: str,
        updated_at: str,
    ) -> Invoice:
        """
        Create an invoice
        """

        response = self.http_client.post('createInvoice', params={
            'number': number,
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'status': status,
            'description': description,
            'hidden_message': hidden_message,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'checkout_url': checkout_url,
            'explorer_url': explorer_url,
            'expires_at': expires_at,
            'created_at': created_at,
            'updated_at': updated_at,
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
        message: str,
        success: bool
    ) -> Transfer:
        """
        Transfer funds between internal wallets.
        Off-chain operation.
        """

        response = self.http_client.post('transfer', params={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'username': username,
            'message': message,
            'success': success
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
        message: str,
        success: bool
    ) -> Withdraw:
        """
        Withdraw funds from merchant wallet to external wallet.
        On-chain operation.
        """
        response = self.http_client.post('withdraw', params={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'to_address': to_address,
            'message': message,
            'success': success
        })
        validate_response(response)
        return Withdraw.from_json(response.json())

    def getWithdrawFee(
        self,
        asset: str,
        blockchain: str,
        network: str,
        amount: float,
        to_address: str,
        message: str,
        blockchain_fee: float,
        processing_fee: float,
        total: float
    ) -> Withdraw:
        """
        Get estimated withdraw fee, composed of blockchain fee and processing fee.
        """
        response = self.http_client.post('getWithdrawFee', params={
            'asset': asset,
            'blockchain': blockchain,
            'network': network,
            'amount': amount,
            'to_address': to_address,
            'message': message,
            'blockchain_fee': blockchain_fee,
            'processing_fee': processing_fee,
            'total': total,
        })
        validate_response(response)
        return Withdraw.from_json(response.json())
